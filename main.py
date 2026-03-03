import streamlit as st
import cv2
import time
import numpy as np
import pandas as pd
from ultralytics import YOLO
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.linear_model import LinearRegression

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Smart Traffic System", layout="wide")
st.title("🚦 AI-Based 4 Lane Smart Traffic Management System")

# ---------------- LOAD YOLO MODEL ----------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# ---------------- SIDEBAR ----------------
st.sidebar.header("System Controls")
camera_on = st.sidebar.checkbox("Enable Camera Detection")
emergency_lane = st.sidebar.selectbox(
    "🚑 Emergency Vehicle Lane Override",
    ["None", "Lane 1", "Lane 2", "Lane 3", "Lane 4"]
)

# ---------------- VEHICLE DETECTION ----------------
def detect_vehicles(frame):
    results = model(frame)
    count = 0
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]
            if label in ["car", "truck", "bus", "motorcycle"]:
                count += 1
    return count

# ---------------- INITIALIZE SESSION ----------------
if "current_lane" not in st.session_state:
    st.session_state.current_lane = 0

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- CAMERA LOGIC ----------------
lane_counts = [0, 0, 0, 0]

if camera_on:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        total_detected = detect_vehicles(frame)
        # Simulate 4 lane split
        lane_counts = np.random.multinomial(total_detected, [0.25]*4)
        st.image(frame, channels="BGR")
    cap.release()
else:
    lane_counts = [
        st.sidebar.number_input("Lane 1 Vehicles", 0, 500, 100),
        st.sidebar.number_input("Lane 2 Vehicles", 0, 500, 150),
        st.sidebar.number_input("Lane 3 Vehicles", 0, 500, 80),
        st.sidebar.number_input("Lane 4 Vehicles", 0, 500, 200),
    ]

# ---------------- EMISSION CALCULATION ----------------
EMISSION_FACTOR = 2.3  # grams per vehicle per cycle
emissions = [count * EMISSION_FACTOR for count in lane_counts]

# ---------------- AI PREDICTION MODEL ----------------
def predict_next(values):
    if len(values) < 4:
        return values[-1] if values else 0
    X = np.arange(len(values)).reshape(-1,1)
    y = np.array(values)
    model_lr = LinearRegression().fit(X,y)
    return int(model_lr.predict([[len(values)]])[0])

predicted = predict_next([sum(lane_counts)])

# ---------------- SIGNAL TIMING ----------------
BASE_TIME = 15
FACTOR = 0.2
green_times = [int(BASE_TIME + count * FACTOR) for count in lane_counts]

current = st.session_state.current_lane

# Emergency override
if emergency_lane != "None":
    current = int(emergency_lane.split()[-1]) - 1
    green_times[current] = 60

# ---------------- DASHBOARD ----------------
cols = st.columns(4)

for i in range(4):
    with cols[i]:
        st.subheader(f"Lane {i+1}")
        st.metric("Vehicles", lane_counts[i])
        st.metric("Green Time", green_times[i])
        st.metric("CO₂ Emission (g)", emissions[i])

        if i == current:
            st.success("🟢 GREEN")
        else:
            st.error("🔴 RED")

# ---------------- LIVE GRAPH ----------------
st.markdown("---")
st.subheader("📈 Live Congestion Graph")

st.session_state.history.append(sum(lane_counts))

fig, ax = plt.subplots()
ax.plot(st.session_state.history)
ax.set_xlabel("Cycle")
ax.set_ylabel("Total Vehicles")
st.pyplot(fig)

# ---------------- DATA LOGGING ----------------
data = {
    "Time": datetime.now(),
    "Lane1": lane_counts[0],
    "Lane2": lane_counts[1],
    "Lane3": lane_counts[2],
    "Lane4": lane_counts[3],
    "Total": sum(lane_counts),
    "Predicted_Next": predicted
}

df = pd.DataFrame([data])
df.to_csv("traffic_log.csv", mode="a", header=not pd.io.common.file_exists("traffic_log.csv"), index=False)

st.success("💾 Data Logged to traffic_log.csv")

# ---------------- TIMER ----------------
st.markdown("---")
st.subheader(f"⏱ Active Lane {current+1} Timer")

progress = st.progress(0)

for sec in range(green_times[current]):
    time.sleep(1)
    progress.progress((sec+1)/green_times[current])

# Move to next lane if no emergency
if emergency_lane == "None":
    st.session_state.current_lane = (current + 1) % 4

st.rerun()
