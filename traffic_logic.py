class TrafficController:
def __init__(self):
self.lanes = ["North", "South", "East", "West"]


def update(self, detections):
count = len(detections)


# Simple adaptive logic
if count > 15:
signal = "North"
elif count > 10:
signal = "East"
elif count > 5:
signal = "South"
else:
signal = "West"


return signal, count
