import streamlit as st
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="4-Lane Smart Traffic Management",
    layout="wide"
)

# ---------------- SIDEBAR CONTROLS ----------------
st.sidebar.title("🚦 4-Lane Traffic Control Panel")

lane1 = st.sidebar.number_input("Lane 1 Vehicle Count", 0, 500, 120)
lane2 = st.sidebar.number_input("Lane 2 Vehicle Count", 0, 500, 180)
lane3 = st.sidebar.number_input("Lane 3 Vehicle Count", 0, 500, 250)
lane4 = st.sidebar.number_input("Lane 4 Vehicle Count", 0, 500, 90)

refresh_rate = st.sidebar.slider("Auto Refresh (seconds)", 5, 60, 10)
auto_refresh = st.sidebar.checkbox("Enable Auto Refresh")

if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()

# ---------------- STORE LANES ----------------
lanes = {
    "Lane 1": lane1,
    "Lane 2": lane2,
    "Lane 3": lane3,
    "Lane 4": lane4
}

# ---------------- FIND HIGHEST TRAFFIC LANE ----------------
priority_lane = max(lanes, key=lanes.get)
total_vehicles = sum(lanes.values())

# ---------------- TRAFFIC LOGIC FUNCTION ----------------
def traffic_logic(vehicle_count):
    if vehicle_count < 150:
        return "Low", 60, "GREEN", vehicle_count * 1.2
    elif 150 <= vehicle_count <= 300:
        return "Medium", 40, "YELLOW", vehicle_count * 1.8
    else:
        return "High", 90, "RED", vehicle_count * 2.5

# ---------------- TITLE ----------------
st.markdown(
    "<h1 style='text-align:center; color:green;'>4-LANE SMART TRAFFIC SURVEILLANCE SYSTEM</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h4 style='text-align:center;'>AI-Based Traffic Optimization & Emission Reduction</h4>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- DASHBOARD ----------------
cols = st.columns(4)

for i, (lane_name, count) in enumerate(lanes.items()):
    density, timer, signal, emission = traffic_logic(count)

    # Priority logic
    if lane_name == priority_lane:
        signal = "GREEN"
        timer = 90

    with cols[i]:
        st.subheader(lane_name)
        st.metric("Vehicles", count)
        st.metric("Density", density)
        st.metric("Signal", signal)
        st.metric("Timer (sec)", timer)
        st.metric("CO₂ Emission", round(emission, 2))

st.markdown("---")

# ---------------- SUMMARY SECTION ----------------
st.subheader("📊 Traffic Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Vehicles (All Lanes)", total_vehicles)

with col2:
    st.metric("Priority Lane", priority_lane)

with col3:
    avg_emission = sum([traffic_logic(v)[3] for v in lanes.values()])
    st.metric("Total CO₂ Emission", round(avg_emission, 2))

st.markdown("---")

# ---------------- ALERT SYSTEM ----------------
if total_vehicles > 900:
    st.error("🚨 Severe Congestion Detected Across All Lanes!")
elif total_vehicles > 600:
    st.warning("⚠️ High Traffic Volume – Optimizing Signals")
else:
    st.success("✅ Traffic Flow Normal")

st.markdown("---")
st.markdown(
    "<p style='text-align:center;'>System Status: ACTIVE | 4-Lane Real-Time Monitoring Enabled</p>",
    unsafe_allow_html=True
)
