import streamlit as st
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Traffic Dashboard", layout="wide")
st.title("🚦 Smart 4-Lane Traffic Management System")

# ---------------- SESSION STATE ----------------
if "active_lane" not in st.session_state:
    st.session_state.active_lane = 0

if "running" not in st.session_state:
    st.session_state.running = False

if "wait_times" not in st.session_state:
    st.session_state.wait_times = [0, 0, 0, 0]

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

# ---------------- SIGNAL TIME CALCULATION ----------------
BASE_TIME = 15
FACTOR = 0.2

green_times = [int(BASE_TIME + v * FACTOR) for v in lane_counts]

# ---------------- UPDATE WAIT TIMES ----------------
current = st.session_state.active_lane

if st.session_state.running:
    for i in range(4):
        if i != current:
            st.session_state.wait_times[i] += 1
        else:
            st.session_state.wait_times[i] = 0

# ---------------- SMART PRIORITY CALCULATION ----------------
priority_scores = [
    lane_counts[i] * 0.7 + st.session_state.wait_times[i] * 0.3
    for i in range(4)
]

priority_lane = priority_scores.index(max(priority_scores))

# ---------------- DASHBOARD TABLE ----------------
st.markdown("---")

columns = st.columns(8)

headers = [
    "Lane",
    "Vehicles",
    "Wait Time (sec)",
    "Priority Score",
    "Priority",
    "Signal",
    "Green Time (sec)",
    "CO₂ Emission (g)"
]

for col, header in zip(columns, headers):
    col.markdown(f"**{header}**")

EMISSION_FACTOR = 2.5
emissions = [v * EMISSION_FACTOR for v in lane_counts]

for i in range(4):

    signal = "🟢 GREEN" if i == current and st.session_state.running else "🔴 RED"

    row = st.columns(8)

    row[0].write(f"Lane {i+1}")
    row[1].write(lane_counts[i])
    row[2].write(st.session_state.wait_times[i])
    row[3].write(round(priority_scores[i], 2))
    row[4].write("⭐ YES" if i == priority_lane else "No")
    row[5].write(signal)
    row[6].write(green_times[i])
    row[7].write(emissions[i])

# ---------------- ALERT SECTION ----------------
st.markdown("---")
st.subheader("🚨 Alerts")

if max(st.session_state.wait_times) > 60:
    st.error("One lane waiting too long! Immediate signal adjustment needed.")
elif max(lane_counts) > 350:
    st.warning("Heavy congestion detected.")
else:
    st.success("Traffic Flow Normal")

# ---------------- SIGNAL TIMER ----------------
if st.session_state.running:

    timer = green_times[current]

    st.markdown("---")
    st.subheader(f"⏱ Lane {current+1} Green Timer")

    progress = st.progress(0)

    for sec in range(timer):
        time.sleep(1)
        progress.progress((sec + 1) / timer)

    # Switch to highest priority lane next
    st.session_state.active_lane = priority_lane
    st.rerun()

else:
    st.info("System Stopped. Press Start to Resume.")
