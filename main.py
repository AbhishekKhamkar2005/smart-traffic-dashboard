import streamlit as st
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Priority Based Smart Traffic", layout="wide")
st.title("🚦 Smart 4-Lane Traffic System (Priority Controlled)")

# ---------------- SESSION STATE ----------------
if "running" not in st.session_state:
    st.session_state.running = False

if "wait_times" not in st.session_state:
    st.session_state.wait_times = [0, 0, 0, 0]

if "active_lane" not in st.session_state:
    st.session_state.active_lane = None

# ---------------- SIDEBAR INPUT ----------------
st.sidebar.header("Traffic Control Panel")

lane_counts = [
    st.sidebar.number_input("Lane 1 Vehicles", 0, 500, 120),
    st.sidebar.number_input("Lane 2 Vehicles", 0, 500, 200),
    st.sidebar.number_input("Lane 3 Vehicles", 0, 500, 80),
    st.sidebar.number_input("Lane 4 Vehicles", 0, 500, 150),
]

start_button = st.sidebar.button("▶ Start System")
stop_button = st.sidebar.button("⏹ Stop System")

if start_button:
    st.session_state.running = True

if stop_button:
    st.session_state.running = False

# ---------------- PRIORITY SCORE ----------------
priority_scores = [
    lane_counts[i] * 0.6 + st.session_state.wait_times[i] * 0.4
    for i in range(4)
]

# Select lane with highest priority
priority_lane = priority_scores.index(max(priority_scores))

# Set active lane as highest priority
if st.session_state.running:
    st.session_state.active_lane = priority_lane

current = st.session_state.active_lane

# ---------------- GREEN TIME CALCULATION ----------------
BASE_TIME = 15
FACTOR = 0.2
green_times = [int(BASE_TIME + v * FACTOR) for v in lane_counts]

# ---------------- UPDATE WAIT TIMES ----------------
if st.session_state.running and current is not None:
    for i in range(4):
        if i != current:
            st.session_state.wait_times[i] += 1
        else:
            st.session_state.wait_times[i] = 0

# ---------------- EMISSION CALCULATION ----------------
EMISSION_FACTOR = 2.5
emissions = [v * EMISSION_FACTOR for v in lane_counts]

# ---------------- DASHBOARD ----------------
st.markdown("---")

headers = [
    "Lane",
    "Vehicles",
    "Wait Time (sec)",
    "Priority Score",
    "Signal",
    "Green Time (sec)",
    "CO₂ Emission (g)"
]

cols = st.columns(len(headers))
for col, header in zip(cols, headers):
    col.markdown(f"**{header}**")

for i in range(4):
    row = st.columns(len(headers))

    signal = "🟢 GREEN" if i == current and st.session_state.running else "🔴 RED"

    row[0].write(f"Lane {i+1}")
    row[1].write(lane_counts[i])
    row[2].write(st.session_state.wait_times[i])
    row[3].write(round(priority_scores[i], 2))
    row[4].write(signal)
    row[5].write(green_times[i])
    row[6].write(emissions[i])

# ---------------- ALERT SECTION ----------------
st.markdown("---")
st.subheader("🚨 Alerts")

if max(st.session_state.wait_times) > 60:
    st.error("One lane waiting too long! Immediate attention required.")
elif max(lane_counts) > 350:
    st.warning("Heavy congestion detected.")
else:
    st.success("Traffic flow normal.")

# ---------------- SIGNAL TIMER ----------------
if st.session_state.running and current is not None:

    timer = green_times[current]

    st.markdown("---")
    st.subheader(f"⏱ Lane {current+1} Green Timer")

    progress = st.progress(0)

    for sec in range(timer):
        time.sleep(1)
        progress.progress((sec + 1) / timer)

    st.rerun()

else:
    st.info("System Stopped. Press Start to Resume.")
