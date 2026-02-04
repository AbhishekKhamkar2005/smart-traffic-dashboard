import streamlit as st
import cv2
import numpy as np
import pandas as pd
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Smart Traffic Management System",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align:center; color:green;'>SMART TRAFFIC MANAGEMENT SYSTEM</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h4 style='text-align:center;'>One-Time Vehicle Detection Dashboard</h4>",
    unsafe_allow_html=True
)

st.markdown("---")

# ================= LOAD VEHICLE CLASSIFIER =================
car_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_car.xml"
)

# ================= SIDEBAR =================
st.sidebar.header("📷 Camera Control")
capture = st.sidebar.button("Capture Image & Count Vehicles")

vehicle_count = 0
captured_image = None

# ================= CAMERA CAPTURE =================
if capture:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        st.error("Camera not accessible")
    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cars = car_cascade.detectMultiScale(gray, 1.1, 2)

        vehicle_count = len(cars)

        for (x, y, w, h) in cars:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        captured_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# ================= SHOW IMAGE =================
if captured_image is not None:
    st.subheader("📸 Captured Image with Vehicle Detection")
    st.image(captured_image, use_column_width=True)

# ================= CALCULATIONS =================
co2_emission = vehicle_count * 2.5  # estimated
fuel_saved = max(0, 50 - vehicle_count)

# ================= DASHBOARD =================
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🚗 Vehicle Count")
    st.metric("Detected Vehicles", vehicle_count)

with col2:
    st.subheader("🌱 CO₂ Emission")
    st.metric("Estimated CO₂ (ppm)", int(co2_emission))

with col3:
    st.subheader("⛽ Fuel Efficiency")
    st.metric("Fuel Saved (Liters)", fuel_saved)

# ================= CHART =================
st.markdown("---")
st.subheader("📊 Vehicle Count Record")

time_now = datetime.now().strftime("%H:%M:%S")
df = pd.DataFrame({
    "Time": [time_now],
    "Vehicle Count": [vehicle_count]
})

st.bar_chart(df.set_index("Time"))

# ================= FOOTER =================
st.markdown(
    "<p style='text-align:center;'>Single Capture Camera-Based Vehicle Detection</p>",
    unsafe_allow_html=True
)
