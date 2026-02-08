import streamlit as st
import random

# Page configuration
st.set_page_config(
    page_title="Smart Traffic Management System",
    layout="wide"
)

# ---------------- CORE INPUT ----------------
vehicle_count = random.randint(100, 500)

# ---------------- LOGIC BASED ON VEHICLE COUNT ----------------
if vehicle_count < 200:
    traffic_density = "Low"
    average_speed = random.randint(50, 60)
    signal_status = "GREEN"
    signal_timer = 60
    co2_emission = random.randint(200, 300)
    fuel_saved = random.randint(40, 50)
    emission_reduction = random.randint(20, 25)
    emergency_priority = "OFF"
    alert_msg = "✅ Normal traffic flow detected"

elif 200 <= vehicle_count <= 350:
    traffic_density = "Medium"
    average_speed = random.randint(30, 45)
    signal_status = "YELLOW"
    signal_timer = 40
    co2_emission = random.randint(300, 450)
    fuel_saved = random.randint(20, 35)
    emission_reduction = random.randint(10, 20)
    emergency_priority = "ON (Standby)"
    alert_msg = "⚠️ Moderate traffic – emergency ready"

else:
    traffic_density = "High"
    average_speed = random.randint(15, 30)
    signal_status = "RED"
    signal_timer = 90
    co2_emission = random.randint(450, 600)
    fuel_saved = random.randint(5, 20)
    emission_reduction = random.randint(5, 10)
    emergency_priority = "ON (Immediate)"
    alert_msg = "🚨 Heavy traffic – emergency priority activated"

# ---------------- TRAFFIC LIGHT COLORS ----------------
red_light = "#555"
yellow_light = "#555"
green_light = "#555"

if signal_status == "RED":
    red_light = "red"
elif signal_status == "YELLOW":
    yellow_light = "yellow"
else:
    green_light = "green"

# ---------------- TITLE ----------------
st.markdown(
    "<h1 style='text-align:center; color:green;'>SMART TRAFFIC MANAGEMENT SYSTEM</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h4 style='text-align:center;'>Dashboard for Emission Reduction</h4>",
    unsafe_allow_html=True
)

# ---------------- TRAFFIC LIGHT DISPLAY ----------------
st.markdown(
    f"""
    <div style="display:flex; justify-content:center; margin:20px 0;">
        <div style="
            width:90px;
            background:#222;
            padding:15px;
            border-radius:20px;
            box-shadow:0 0 10px rgba(0,0,0,0.6);
        ">
            <div style="width:55px;height:55px;border-radius:50%;background:{red_light};margin:10px auto;"></div>
            <div style="width:55px;height:55px;border-radius:50%;background:{yellow_light};margin:10px auto;"></div>
            <div style="width:55px;height:55px;border-radius:50%;background:{green_light};margin:10px auto;"></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- DASHBOARD LAYOUT ----------------
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
    st.metric("Signal Timer (sec)", signal_timer)
    st.write(f"Emergency Priority: {emergency_priority}")

# Emission Monitoring
with col3:
    st.subheader("🌱 Emission Monitoring")
    st.metric("CO₂ Emission (ppm)", co2_emission)
    st.metric("Fuel Saved (liters)", fuel_saved)
    st.metric("Emission Reduction", f"{emission_reduction} %")

st.markdown("---")

# Alerts Section
st.subheader("🔔 Alerts & Notifications")
st.write(alert_msg)

st.markdown("---")

# Footer
st.markdown(
    "<p style='text-align:center;'>System Status: ACTIVE | Real-Time Monitoring Enabled</p>",
    unsafe_allow_html=True
)
