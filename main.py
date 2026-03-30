# main.py
import cv2
from ultralytics import YOLO
from utils.dynamic_area import get_dynamic_max_area, should_trigger_alert
import config

model = YOLO('models/yolov8n.pt')

cap = cv2.VideoCapture('data/test_videos/test1.mp4')  # or 0 for webcam

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Get dynamic max_area for current frame
    max_area = get_dynamic_max_area(frame.shape, setting='medium')

    results = model(frame, conf=config.CONFIDENCE_THRESHOLD)

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            if cls not in config.TARGET_CLASSES:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            area = (x2 - x1) * (y2 - y1)

            if should_trigger_alert(area, cls):
                # Draw bounding box
                color = (0, 255, 0) if cls == 0 else (0, 165, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                
                label = f"{'Person' if cls==0 else 'Cat' if cls==15 else 'Dog'} {area:.0f}px"
                cv2.putText(frame, label, (x1, y1-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                # Trigger alert (Telegram + Blynk)
                print(f"ALERT: {label} detected in danger zone!")

    cv2.imshow('Guardian AI - Live Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
