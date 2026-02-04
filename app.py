import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="Smart Traffic Management System",
    layout="wide"
)

# Title
st.markdown(
    "<h1 style='text-align:center; color:green;'>SMART TRAFFIC MANAGEMENT SYSTEM</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h4 style='text-align:center;'>Dashboard for Emission Reduction</h4>",
    unsafe_allow_html=True
)

st.markdown("---")

# Generate simulated real-time data
vehicle_count = random.randint(100, 500)
traffic_density = random.choice(["Low", "Medium", "High"])
average_speed = random.randint(20, 60)
co2_emission = random.randint(200, 600)
fuel_saved = random.randint(10, 50)
signal_status = random.choice(["RED", "YELLOW", "GREEN"])

# Dashboard layout
col1, col2, col3 = st.columns(3)

# Traffic Flow Overview
with col1:
    st.subheader("🚦 Traffic Flow Overview")
    st.metric("Vehicle Count", vehicle_count)
    st.metric("Traffic Density", traffic_density)
    st.metric("Average Speed (km/h)", average_speed)

# Signal Status
with col2:
    st.subheader("🚥 Traffic Signal Status")
    st.metric("Current Signal", signal_status)
    st.metric("Signal Timer (sec)", random.randint(10, 60))
    st.write("Emergency Priority: OFF")

# Emission Monitoring
with col3:
    st.subheader("🌱 Emission Monitoring")
    st.metric("CO₂ Emission (ppm)", co2_emission)
    st.metric("Fuel Saved (liters)", fuel_saved)
    st.metric("Emission Reduction", f"{random.randint(5,25)} %")

st.markdown("---")

# Alerts Section
st.subheader("🔔 Alerts & Notifications")
alerts = [
    "High traffic detected at Junction A",
    "Normal traffic flow at Junction B",
    "High emission levels detected in City Center",
    "Traffic signals operating normally"
]
st.write(random.choice(alerts))

st.markdown("---")

# Footer
st.markdown(
    "<p style='text-align:center;'>System Status: ACTIVE | Real-Time Monitoring Enabled</p>",
    unsafe_allow_html=True
)
import cv2
import streamlit as st
import numpy as np

# Load pre-trained model
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Function to detect vehicles
def detect_vehicles(frame):
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(net.getUnconnectedOutLayersNames())
    vehicles = 0
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] == "car":
                vehicles += 1
    return vehicles

# Capture video feed
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect vehicles
    vehicles = detect_vehicles(frame)
    
    # Update dashboard
    st.write(f"Vehicle Count: {vehicles}")
    
    # Display frame
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
