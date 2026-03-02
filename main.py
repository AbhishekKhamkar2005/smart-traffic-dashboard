import streamlit as st
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Traffic Management System",
    layout="wide"
)

# ---------------- AUTO REFRESH ----------------
refresh_rate = st.sidebar.slider("Auto Refresh (seconds)", 5, 60, 10)
auto_refresh = st.sidebar.checkbox("Enable Auto Refresh")

if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()

# ---------------- VEHICLE INPUT ----------------
st.sidebar.title("Traffic Input Control")
vehicle_count = st.sidebar.number_input(
    "Enter Vehicle Count",
    min_value=0,
    max_value=1000,
    value=250
)

# ---------------- LOGIC ----------------
if vehicle_count < 200:
    traffic_density = "Low"
    average_speed = 55
    signal_status = "GREEN"
    signal_timer = 60
    co2_emission = vehicle_count * 1.2
    fuel_saved = vehicle_count * 0.3
    emission_reduction = 25
    emergency_priority = "OFF"
    alert_msg = "✅ Normal traffic flow detected"

elif 200 <= vehicle_count <= 350:
    traffic_density = "Medium"
    average_speed = 40
    signal_status = "YELLOW"
    signal_timer = 40
    co2_emission = vehicle_count * 1.8
    fuel_saved = vehicle_count * 0.2
    emission_reduction = 15
    emergency_priority = "ON (Standby)"
    alert_msg = "⚠️ Moderate traffic – emergency ready"

else:
    traffic_density = "High"
    average_speed = 25
    signal_status = "RED"
    signal_timer = 90
    co2_emission = vehicle_count * 2.5
    fuel_saved = vehicle_count * 0.1
    emission_reduction = 8
    emergency_priority = "ON (Immediate)"
    alert_msg = "🚨 Heavy traffic – emergency priority activated"

# ---------------- TRAFFIC LIGHT ----------------
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
    "<h4 style='text-align:center;'>AI-Based Emission Reduction Dashboard</h4>",
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

# ---------------- DASHBOARD ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🚦 Traffic Flow Overview")
    st.metric("Vehicle Count", vehicle_count)
    st.metric("Traffic Density", traffic_density)
    st.metric("Average Speed (km/h)", average_speed)

with col2:
    st.subheader("🚥 Traffic Signal Status")
    st.metric("Current Signal", signal_status)
    st.metric("Signal Timer (sec)", signal_timer)
    st.write(f"Emergency Priority: {emergency_priority}")

with col3:
    st.subheader("🌱 Emission Monitoring")
    st.metric("CO₂ Emission (ppm)", round(co2_emission, 2))
    st.metric("Fuel Saved (liters)", round(fuel_saved, 2))
    st.metric("Emission Reduction", f"{emission_reduction}%")

st.markdown("---")

st.subheader("🔔 Alerts & Notifications")
st.success(alert_msg)

st.markdown("---")
st.markdown(
    "<p style='text-align:center;'>System Status: ACTIVE | Real-Time Monitoring Enabled</p>",
    unsafe_allow_html=True
)
