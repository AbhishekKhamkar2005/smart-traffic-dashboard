import streamlit as st
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Alternate Smart Signal System", layout="wide")

st.title("🚦 4-Lane Alternate Smart Traffic Signal System")
st.markdown("Signal changes automatically based on vehicle count & time duration")

# ---------------- INPUT VEHICLE COUNTS ----------------
st.sidebar.header("Traffic Input")

lane_counts = [
    st.sidebar.number_input("Lane 1 Vehicles", 0, 500, 120),
    st.sidebar.number_input("Lane 2 Vehicles", 0, 500, 200),
    st.sidebar.number_input("Lane 3 Vehicles", 0, 500, 80),
    st.sidebar.number_input("Lane 4 Vehicles", 0, 500, 150),
]

# ---------------- SIGNAL TIME CALCULATION ----------------
BASE_TIME = 20          # minimum green time
FACTOR = 0.2            # extra time per vehicle

green_times = [int(BASE_TIME + count * FACTOR) for count in lane_counts]

# ---------------- SESSION STATE FOR ROTATION ----------------
if "current_lane" not in st.session_state:
    st.session_state.current_lane = 0

# ---------------- AUTO SIGNAL ROTATION ----------------
current = st.session_state.current_lane

# Display dashboard
cols = st.columns(4)

for i in range(4):
    with cols[i]:
        st.subheader(f"Lane {i+1}")
        st.metric("Vehicles", lane_counts[i])
        st.metric("Green Time (sec)", green_times[i])

        if i == current:
            st.success("🟢 GREEN")
        else:
            st.error("🔴 RED")

st.markdown("---")

st.subheader("⏱ Active Signal Timer")

progress_bar = st.progress(0)

# Run timer for active lane
for sec in range(green_times[current]):
    time.sleep(1)
    progress_bar.progress((sec + 1) / green_times[current])

# After timer ends → switch lane
st.session_state.current_lane = (current + 1) % 4
st.rerun()
