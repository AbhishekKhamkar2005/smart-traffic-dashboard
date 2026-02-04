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
    "<h4 style='text-align:center;'>Live Vehicle Detection & Emission Dashboard</h4>",
    unsafe_allow_html=True
)

st.markdown("---")

# ================= LOAD VEHICLE CLASSIFIER =================
car_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_car.xml"
)

# ================= CAMERA INPUT =================
st.sidebar.header("📷 Live Camera Control")
run_camera = st.sidebar.checkbox("Start Camera")

FRAME_WINDOW = st.image([])

vehicle_count = 0

if run_camera:
    cap = cv2.VideoCapture(0)

    while run_camera:
        ret, frame = cap.read()
        if not ret:
            st.error("Camera not accessible")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cars = car_cascade.detectMultiScale(gray, 1.1, 2)

        vehicle_count = len(cars)

        for (x, y, w, h) in cars:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)

        if not st.sidebar.checkbox("Keep Running", value=True):
            break

    cap.release()

# ================= EMISSION CALCULATION =================
co2_emission = vehicle_count * 2.5   # estimated ppm
fuel_saved = max(0, 50 - vehicle_count)

# ================= DASHBOARD =================
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🚗 Vehicle Detection")
    st.metric("Live Vehicle Count", vehicle_count)

with col2:
    st.subheader("🌱 Emission Estimation")
    st.metric("CO₂ Emission (ppm)", int(co2_emission))

with col3:
    st.subheader("⛽ Fuel Efficiency")
    st.metric("Fuel Saved (L)", fuel_saved)

# ================= LIVE CHART =================
st.markdown("---")
st.subheader("📊 Live Vehicle Count Chart")

time_now = datetime.now().strftime("%H:%M:%S")
df = pd.DataFrame({
    "Time": [time_now],
    "Vehicle Count": [vehicle_count]
})

st.line_chart(df.set_index("Time"))

# ================= FOOTER =================
st.markdown(
    "<p style='text-align:center;'>Live Camera-Based Vehicle Detection Using Computer Vision</p>",
    unsafe_allow_html=True
)
