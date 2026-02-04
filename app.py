import streamlit as st
import time
import pandas as pd
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Smart Traffic Management System",
    layout="wide"
)

# ================= AUTO REFRESH =================
REFRESH_INTERVAL = 5  # seconds
time.sleep(REFRESH_INTERVAL)
st.experimental_rerun()

# ================= TITLE =================
st.markdown(
    "<h1 style='text-align:center; color:green;'>SMART TRAFFIC MANAGEMENT SYSTEM</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h4 style='text-align:center;'>Live Dashboard for Emission Reduction</h4>",
    unsafe_allow_html=True
)

st.markdown("---")

# ================= SIDEBAR CONTROLS =================
st.sidebar.header("⚙️ Control Panel")

vehicle_count = st.sidebar.slider("Vehicle Count", 0, 1000, 300)
traffic_density = st.sidebar.selectbox("Traffic Density", ["Low", "Medium", "High"])
signal_status = st.sidebar.selectbox("Traffic Signal", ["RED", "YELLOW", "GREEN"])
co2_emission = st.sidebar.slider("CO₂ Emission (ppm)", 100, 1000, 400)

# ================= LOGIC =================
if traffic_density == "Low":
    avg_speed = 60
    fuel_saved = 40
elif traffic_density == "Medium":
    avg_speed = 40
    fuel_saved = 25
else:
    avg_speed = 20
    fuel_saved = 10

emission_reduction = max(0, 100 - (co2_emission // 10))

# ================= METRICS =================
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🚦 Traffic Overview")
    st.metric("Vehicle Count", vehicle_count)
    st.metric("Traffic Density", traffic_density)
    st.metric("Avg Speed (km/h)", avg_speed)

with col2:
    st.subheader("🚥 Signal Status")
    st.metric("Signal", signal_status)
    st.metric("Timer (sec)", 30)

with col3:
    st.subheader("🌱 Emission Status")
    st.metric("CO₂ (ppm)", co2_emission)
    st.metric("Fuel Saved (L)", fuel_saved)
    st.metric("Emission Reduction", f"{emission_reduction} %")

st.markdown("---")

# ================= LIVE DATA =================
current_time = datetime.now().strftime("%H:%M:%S")

data = {
    "Time": [current_time],
    "Vehicles": [vehicle_count],
    "CO₂ Emission": [co2_emission],
    "Fuel Saved": [fuel_saved]
}

df = pd.DataFrame(data)

# ================= LIVE CHARTS =================
st.subheader("📊 Live Traffic & Emission Charts")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.write("### Vehicle Count (Live)")
    st.line_chart(df.set_index("Time")["Vehicles"])

with chart_col2:
    st.write("### CO₂ Emission vs Fuel Saved")
    st.bar_chart(df.set_index("Time")[["CO₂ Emission", "Fuel Saved"]])

# ================= ALERTS =================
st.markdown("---")
st.subheader("🔔 Alerts")

if traffic_density == "High":
    st.error("High Traffic Congestion Detected!")
elif co2_emission > 700:
    st.warning("High Emission Level Detected!")
else:
    st.success("Traffic Conditions Normal")

# ================= FOOTER =================
st.markdown(
    "<p style='text-align:center;'>Auto Refresh: Every 5 Seconds | Live Simulation Mode</p>",
    unsafe_allow_html=True
)
