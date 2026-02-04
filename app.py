import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image

# Page config
st.set_page_config(page_title="Vehicle Counter", layout="centered")
st.title("🚦 Vehicle Counting from Image")

# Load YOLOv8 model (pretrained)
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")  # nano model (fast & light)

model = load_model()

# Vehicle classes in COCO dataset
VEHICLE_CLASSES = ["car", "bus", "truck", "motorcycle"]

uploaded_file = st.file_uploader(
    "Upload a road image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    # Read image
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("🔍 Detect & Count Vehicles"):
        results = model(img_array)[0]

        vehicle_count = 0

        for box in results.boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]

            if class_name in VEHICLE_CLASSES:
                vehicle_count += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(
                    img_array,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )
                cv2.putText(
                    img_array,
                    class_name,
                    (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        st.success(f"🚗 Total Vehicles Detected: **{vehicle_count}**")
        st.image(img_array, caption="Detected Vehicles", use_column_width=True)
