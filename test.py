import cv2
from ultralytics import YOLO

# --- 1. 初始化 YOLO 模型 ---
model = YOLO('yolov8n.pt')

# --- 2. 讀取電腦中的影片檔 ---
# 請替換成妳的影片檔名
video_path = 'testvideo1.mp4' 
cap = cv2.VideoCapture(video_path)

# ---------------------------------------------------------
# 🛠️ 參數微調區 (Tuning Parameters) - 針對不同目標設定專屬面積
# ---------------------------------------------------------
ALERT_LINE_Y = 300     # 虛擬警戒線的高度

# 建立一個字典，為每個類別 (Class ID) 設定不同的最小面積
# 數字需要妳根據影片實際測試來微調！
MIN_AREA_DICT = {
    0: 25000,   # 人 (Person) 體型大，面積設定比較大
    15: 6000,   # 貓 (Cat) 體型小，面積設定比較小
    16: 6000   # 狗 (Dog) 體型中等，面積設定居中
}

print(f"🚀 YOLO 邏輯影片測試啟動！(具備專屬體型比例)")

while cap.isOpened():
    success, frame = cap.read()
    if not success: 
        print("影片播放完畢，測試結束。")
        break

    # --- 3. 執行 YOLO 偵測 ---
    results = model(frame, classes=[0, 15, 16], verbose=False)
    
    # --- 4. 分析目標 ---
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]
        
        # (A) 計算實際面積
        width = x2 - x1
        height = y2 - y1
        area = width * height
        bottom_y = y2
        
        # (B) 🌟 核心修改：從字典中找出這個目標「專屬」的最低標準
        # 如果找不到對應的 ID（預防萬一），就預設為 25000
        required_area = MIN_AREA_DICT.get(cls_id, 25000)
        
        # 畫出預設的綠框，並在畫面上顯示「當前面積 / 需要的面積」方便妳除錯
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, f"{class_name} ({int(area)}/{required_area})", (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # (C) 判斷條件：當前面積 > 專屬設定面積 AND 踩進警戒線
        if area > required_area and bottom_y > ALERT_LINE_Y:
            
            # 視覺化除錯：將框框改成紅色
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
            cv2.putText(frame, "!!! DANGER !!!", (int(x1), int(y2)+25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            print(f"⚠️ 發現 {class_name} 進入危險區！面積達標: {int(area)} > {required_area}")

    # --- 5. 畫出警戒線 ---
    cv2.line(frame, (0, ALERT_LINE_Y), (frame.shape[1], ALERT_LINE_Y), (0, 255, 255), 2)

    cv2.imshow("YOLO Logic Test (Smart Area)", frame)
    
    if cv2.waitKey(15) & 0xFF == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()
