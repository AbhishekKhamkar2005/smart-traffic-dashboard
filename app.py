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

st.subheader("🔔 Alerts & Notifications")

if vehicle_count < 200:
    alert_msg = "✅ Normal traffic flow detected"
elif 200 <= vehicle_count <= 350:
    alert_msg = "⚠️ Moderate traffic – monitor closely"
else:
    alert_msg = "🚨 Heavy traffic congestion detected – action required"

st.write(alert_msg)

st.markdown("---")

# Footer
st.markdown(
    "<p style='text-align:center;'>System Status: ACTIVE | Real-Time Monitoring Enabled</p>",
    unsafe_allow_html=True
)
