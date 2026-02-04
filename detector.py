import cv2
import pandas as pd
from ultralytics import YOLO
from datetime import datetime
import time
import os

# Load AI Model
model = YOLO('yolov8n.pt') 

# Open CCTV/Webcam
cap = cv2.VideoCapture(0)

print("AI Detector Started... Press 'q' to stop.")

# Create CSV with headers if it doesn't exist
csv_path = 'traffic_log.csv'
if not os.path.exists(csv_path):
    pd.DataFrame(columns=['Timestamp', 'Vehicle_Count']).to_csv(csv_path, index=False)

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # AI Detection (Classes 2, 3, 5, 7 = car, motorcycle, bus, truck)
    results = model(frame, classes=[2, 3, 5, 7], verbose=False)
    vehicle_count = len(results[0].boxes)

    # Log to CSV
    log_entry = pd.DataFrame([[datetime.now().strftime("%H:%M:%S"), vehicle_count]])
    log_entry.to_csv(csv_path, mode='a', index=False, header=False)

    # Show Camera Feed
    annotated_frame = results[0].plot()
    cv2.putText(annotated_frame, f"Count: {vehicle_count}", (20, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("CCTV Traffic AI", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()