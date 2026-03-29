import os
import platform

# --- 1. 修正 Windows 錯誤 (Fix Windows Error) ---
if not hasattr(os, 'uname'):
    def mock_uname():
        return ("Windows", "PC", "Version", "1.0", "x86_64")
    os.uname = mock_uname

import BlynkLib
from ultralytics import YOLO
import cv2
import requests
import time

# --- 2. Blynk & Telegram 設定 (Credentials) ---
BLYNK_AUTH_TOKEN = "FHWjfgSeC9LcONVAUkbEqMyM9ql_Ig3G"
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN, server="blynk.cloud")

TOKEN = "8354207024:AAEmDrqOoJzySiTQI2YOodtK9DMJMuCMVMI"
CHAT_ID = "6795273501"

# --- 3. 無線鏡頭與 AI 設定 (Camera & AI) ---
video_url = "http://10.11.33.180:8080/video" 
cap = cv2.VideoCapture(video_url)
model = YOLO('yolov8n.pt')

last_telegram_time = 0

# ---------------------------------------------------------
# 🛠️ [進階設定] 針對不同目標設定專屬面積與警戒線
# ---------------------------------------------------------
ALERT_LINE_Y = 200     # 虛擬警戒線的高度 (Y座標)

# 字典：為不同類別設定專屬的最少觸發面積 (請依照實際架設環境微調)
MIN_AREA_DICT = {
    0: 30000,   # 人 (Person) 體型大
    15: 8000,   # 貓 (Cat) 體型小
    16: 12000   # 狗 (Dog) 體型中等
}

print("系統啟動成功！具備「動態體型比例」與「區域過濾」功能...")

while cap.isOpened():
    blynk.run() 
    
    success, frame = cap.read()
    if not success: 
        print("連線中斷，請檢查手機 IP Webcam")
        break

    # 執行 YOLO 偵測，只找人(0)、貓(15)、狗(16)
    results = model(frame, classes=[0, 15, 16], verbose=False)
    
    danger_detected = False # 預設目前沒有危險
    
    # --- 4. 分析畫面中的每一個目標 ---
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]
        
        # (A) 計算實際面積與腳底位置
        width = x2 - x1
        height = y2 - y1
        area = width * height
        bottom_y = y2
        
        # (B) 從字典找出專屬標準 (若找不到則預設 25000 防呆)
        required_area = MIN_AREA_DICT.get(cls_id, 25000)
        
        # (C) 判斷條件：面積達標 AND 踩進警戒線
        if area > required_area and bottom_y > ALERT_LINE_Y:
            danger_detected = True
            
            # 視覺化除錯：紅框 + 顯示 DANGER
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 3)
            cv2.putText(frame, f"DANGER! {class_name}", (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        else:
            # 尚未達標：畫綠框方便觀察面積數字
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"{class_name} ({int(area)}/{required_area})", (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # --- 5. 根據分析結果，觸發外部警報 ---
    if danger_detected:
        # (A) Blynk：讓手機 App 的 LED 亮起紅色
        blynk.virtual_write(1, 255) 
        
        current_time = time.time()
        # (B) Telegram：發送大聲的聲音通知 (設定 10 秒冷卻避免洗版)
        if current_time - last_telegram_time > 10:
            print("!!! 發現危險目標：發送 Telegram 警報 !!!")
            tg_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=⚠️ 警告！發現人或貓狗進入危險區域！"
            try: 
                requests.get(tg_url, timeout=5)
            except: 
                pass
            last_telegram_time = current_time 
    else:
        # 安全時：關閉 Blynk 的 LED 燈
        blynk.virtual_write(1, 0)

    # --- 6. 畫出虛擬警戒線 ---
    cv2.line(frame, (0, ALERT_LINE_Y), (frame.shape[1], ALERT_LINE_Y), (0, 255, 255), 2)
    cv2.putText(frame, f"Tripwire (Y={ALERT_LINE_Y})", (10, ALERT_LINE_Y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # 顯示最終監控畫面
    cv2.imshow("GuardianAI Real-time Monitor", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()
