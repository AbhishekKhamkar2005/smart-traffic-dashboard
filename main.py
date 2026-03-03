import streamlit as st
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Continuous Smart Signal System", layout="wide")

st.title("🚦 Continuous 4-Lane Smart Traffic Signal System")
st.markdown("Signal changes continuously based on vehicle count & adaptive timing")

# ---------------- INPUT SECTION ----------------
st.sidebar.header("Traffic Input (Live Adjustable)")

lane_counts = [
    st.sidebar.number_input("Lane 1 Vehicles", 0, 500, 120),
    st.sidebar.number_input("Lane 2 Vehicles", 0, 500, 250),
    st.sidebar.number_input("Lane 3 Vehicles", 0, 500, 80),
    st.sidebar.number_input("Lane 4 Vehicles", 0, 500, 150),
]

BASE_TIME = 15     # minimum green time
FACTOR = 0.25      # time increase per vehicle

# Calculate green times dynamically
green_times = [int(BASE_TIME + count * FACTOR) for count in lane_counts]

# ---------------- SESSION STATE ----------------
if "current_lane" not in st.session_state:
    st.session_state.current_lane = 0

if "running" not in st.session_state:
    st.session_state.running = True

# ---------------- DASHBOARD FUNCTION ----------------
def display_dashboard(active_lane):
    cols = st.columns(4)
    for i in range(4):
        with cols[i]:
            st.subheader(f"Lane {i+1}")
            st.metric("Vehicles", lane_counts[i])
            st.metric("Green Time (sec)", green_times[i])

            if i == active_lane:
                st.success("🟢 GREEN")
            else:
                st.error("🔴 RED")

# ---------------- CONTINUOUS LOOP ----------------
while st.session_state.running:

    current = st.session_state.current_lane

    display_dashboard(current)

    st.markdown("---")
    st.subheader(f"⏱ Lane {current+1} Active Timer")

    progress = st.progress(0)

    for sec in range(green_times[current]):
        time.sleep(1)
        progress.progress((sec + 1) / green_times[current])

    # Move to next lane
    st.session_state.current_lane = (current + 1) % 4
    st.rerun()
