from ultralytics import YOLO


class VehicleDetector:
def __init__(self):
self.model = YOLO("yolov8n.pt")
self.allowed = {"car", "bus", "truck", "motorcycle"}


def detect(self, frame):
results = self.model(frame, stream=True, conf=0.4)
detections = []


for r in results:
for box in r.boxes:
cls = int(box.cls[0])
label = self.model.names[cls]


if label in self.allowed:
x1, y1, x2, y2 = map(int, box.xyxy[0])
detections.append((x1, y1, x2, y2, label))


return detections
