import cv2
from detector import VehicleDetector
from traffic_logic import TrafficController


# Camera source: 0 = webcam, or IP camera URL
CAMERA_SOURCE = 0


def main():
cap = cv2.VideoCapture(CAMERA_SOURCE)
detector = VehicleDetector()
controller = TrafficController()


while True:
ret, frame = cap.read()
if not ret:
break


detections = detector.detect(frame)
signal, counts = controller.update(detections)


# Draw detections
for (x1, y1, x2, y2, label) in detections:
cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
cv2.putText(frame, label, (x1, y1 - 10),
cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


cv2.putText(frame, f"GREEN SIGNAL: {signal}", (20, 40),
cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)


cv2.imshow("Smart Traffic Management", frame)


if cv2.waitKey(1) & 0xFF == ord('q'):
break


cap.release()
cv2.destroyAllWindows()


if __name__ == "__main__":
main()
