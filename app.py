import streamlit as st
import pandas as pd
import numpy as np 
import pickle 
import json 
import os 
from datetime import datetime 
from sklearn.model_selection import train_test_split 
# Load the trained regression model
with open("models/ev_demand_model.pkl", "rb") as file:
    model = pickle.load(file)

st.set_page_config(
    page_title="VoltIQ | Smart EV Grid",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# ---------- CUSTOM DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #081225 0%, #101b35 55%, #102b35 100%);
    color: #F1F5F9;
} 
.stDownloadButton > button {
    background-color: #00E5FF;
    color: #081225;
    border: none;
    border-radius: 10px;
    font-weight: bold;
}

.stDownloadButton > button:hover {
    background-color: #00B8D4;
    color: #081225;
} 
[data-testid="stSidebar"] {
    background: #0B1427;
    border-right: 1px solid #243650;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}
h1, h2, h3, p, label {
    color: #F1F5F9;
}
.hero {
    background: linear-gradient(115deg, #123B45, #17264B 65%, #27306B);
    border: 1px solid #2E6971;
    border-radius: 22px;
    padding: 28px;
    margin-bottom: 24px;
}
.eyebrow {
    color: #52F2BC;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 3px;
}
.hero-title {
    font-size: 38px;
    font-weight: 850;
    line-height: 1.2;
    margin: 12px 0;
}
.hero-sub {
    color: #C3D3E8;
    font-size: 16px;
}
.metric-card {
    background: linear-gradient(145deg, #172740, #101D32);
    border: 1px solid #30435D;
    border-radius: 16px;
    padding: 20px;
    min-height: 135px;
}
.metric-label {
    color: #A8BDD3;
    font-size: 13px;
    font-weight: 700;
}
.metric-value {
    color: #57F3BE;
    font-size: 29px;
    font-weight: 850;
    margin-top: 10px;
}
.metric-note {
    color: #9BAFC5;
    font-size: 12px;
    margin-top: 5px;
}
.section-card {
    background: #111F35;
    border: 1px solid #2B405C;
    border-radius: 18px;
    padding: 20px;
    margin-top: 12px;
}
.pill {
    display: inline-block;
    background: #153E3B;
    color: #65F4C5;
    padding: 7px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}
div.stButton > button {
    background: linear-gradient(90deg, #21D9A0, #42B8E8);
    color: #071426;
    border: 0;
    border-radius: 10px;
    font-weight: 800;
    min-height: 45px;
}
div.stButton > button:hover {
    border: 1px solid #FFFFFF;
    color: #071426;
} 
header[data-testid="stHeader"] {
    background-color: #0b1428 !important;
}

[data-testid="stToolbar"] {
    background-color: #0b1428 !important;
}

.stAppHeader {
    background-color: #0b1428 !important;
}

[data-testid="stDecoration"] {
    display: none !important;
} 
.stAppHeader,
header[data-testid="stHeader"],
[data-testid="stToolbar"] {
    background: #0b1428 !important;
    color: #0b1428 !important;
    box-shadow: none !important;
}

.stAppHeader::before {
    background: #0b1428 !important;
} 
</style> 

""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## ⚡ VoltIQ")
    st.caption("SMART GRID INTELLIGENCE")
    st.divider()

    st.markdown("### 🎛️ Charging controls")

    hour = st.slider("Hour of day", 0, 23, 18)
    temperature = st.slider("Temperature (°C)", -5, 45, 28)
    sessions = st.slider("Expected charging sessions", 1, 100, 25)
    energy_per_session = st.slider(
        "Average energy per session (kWh)", 5, 60, 20
    )
    capacity = st.slider(
        "Hourly grid capacity (kWh)", 100, 2000, 600, step=50
    )
    base_tariff = st.slider(
        "Base tariff (₹/kWh)", 3.0, 30.0, 8.0, step=0.5
    )

    st.divider()
    st.caption("Prototype • Demo calculations")

# ---------- DEMO CALCULATION ----------
# These calculations are illustrative, not trained ML predictions.
peak_factor = 1.25 if hour in range(7, 11) or hour in range(17, 22) else 0.75

if temperature < 10:
    weather_factor = 1.12
elif temperature > 32:
    weather_factor = 1.10
else:
    weather_factor = 1.0

# Prepare input for the trained ML model
input_data = pd.DataFrame([{ 
    "hour": hour,
    "temperature_c": temperature,
    "charging_sessions": sessions
}]) 

# Predict energy demand using the trained model
predicted_demand = model.predict(input_data)[0] 

# Keep the value non-negative
predicted_demand = max(0, predicted_demand) 
st.success("Prediction completed successfully!")

st.metric(
    label="Predicted Energy Demand",
    value=f"{predicted_demand:.2f} kWh"
) 
# Dynamic Pricing Logic
if predicted_demand <= 50:
    price = 6
elif predicted_demand <= 100:
    price = 8
elif predicted_demand <= 150:
    price = 12
else:
    price = 15

st.metric(
    label="Recommended Charging Price",
    value=f"₹{price}/kWh"
) 
st.subheader("Grid Load Status") 

if predicted_demand < 40:
    st.success("🟢 Low Grid Load - Charging is Normal")
elif predicted_demand < 80:
    st.warning("🟡 Medium Grid Load - Monitor Charging")
else:
    st.error("🔴 High Grid Load - Reduce Peak Charging") 
    st.subheader("Estimated Charging Revenue")

estimated_revenue = predicted_demand * price

st.metric(
    label="Estimated Revenue",
    value=f"₹{estimated_revenue:.2f}"
)  
st.subheader("Current Prediction Summary")

summary = pd.DataFrame([{
    "Predicted Demand (kWh)": round(predicted_demand, 2),
    "Charging Price (₹/kWh)": price,
    "Estimated Revenue (₹)": round(estimated_revenue, 2),
    "Grid Status": (
        "Low" if predicted_demand < 40
        else "Medium" if predicted_demand < 80 
        else "High"
    )
}])

st.dataframe(summary, use_container_width=True) 
history_file = "prediction_history.csv"

if st.button("Save This Prediction"):
    new_record = pd.DataFrame([{
        "Date & Time": datetime.now().strftime("%d-%m-%Y %I:%M:%S %p"),
        "Demand (kWh)": round(predicted_demand, 2),
        "Price (₹/kWh)": price,
        "Estimated Revenue (₹)": round(estimated_revenue, 2)
    }])

    if os.path.exists(history_file):
        new_record.to_csv(
            history_file, mode="a", header=False, index=False
        )
    else:
        new_record.to_csv(history_file, index=False)

    st.success("Prediction saved to history!") 
st.subheader("Prediction History")

if os.path.exists(history_file):
    history = pd.read_csv(history_file)
    st.dataframe(history, use_container_width=True)

    st.download_button(
        label="Download Prediction History",
        data=history.to_csv(index=False),
        file_name="prediction_history.csv",
        mime="text/csv"
    )
else:
    st.info("No prediction history available yet.") 
st.subheader("Model Information") 

st.write("Algorithm: Linear Regression")
st.write("Training dataset: 36 sample records")
st.write("Prediction target: Energy Demand (kWh)")

st.info(
    "This model uses hour, temperature, and charging sessions "
    "to estimate energy demand."
) 

df = pd.read_csv("data/ev_charging_small_dataset.csv")

X = df[["hour", "temperature_c", "charging_sessions"]]
y = df["energy_demand_kwh"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

predictions = model.predict(X_test) 
from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(y_test, predictions)

st.metric("Prediction Error (MAE)", f"{mae:.2f} kWh") 


st.subheader("Actual vs Predicted Demand")

import matplotlib.pyplot as plt

chart_data = pd.DataFrame({
    "Actual Demand": y_test.values,
    "Predicted Demand": predictions
})

st.line_chart(chart_data)
with open("models/model_metrics.json", "r") as file:
    metrics = json.load(file)

st.write("Mean Absolute Error (MAE):", metrics["mae"])
st.write("R² Score:", metrics["r2_score"])
st.caption("Prediction generated by a trained Linear Regression model.")

load_percent = predicted_demand / capacity * 100

if load_percent >= 90:
    status = "HIGH LOAD"
    status_color = "#FF7185"
    suggested_tariff = base_tariff * 1.25
elif load_percent >= 65:
    status = "MODERATE"
    status_color = "#FFD166"
    suggested_tariff = base_tariff * 1.10
else:
    status = "NORMAL"
    status_color = "#57F3BE"
    suggested_tariff = base_tariff

# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <div class="eyebrow">NEXT-GENERATION ENERGY ANALYTICS</div>
    <div class="hero-title">Smart EV Charging<br>Demand Predictor ⚡</div>
    <div class="hero-sub">
        Explore charging demand, monitor grid capacity and
        understand how intelligent pricing could support EV infrastructure.
    </div>
    <br>
    <span class="pill">● INTERACTIVE DEMO</span>
</div>
""", unsafe_allow_html=True)

st.subheader("⚡ Station overview")
st.caption("Change the controls in the sidebar to explore different scenarios.")

# ---------- METRIC CARDS ----------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">ESTIMATED ENERGY DEMAND</div>
      <div class="metric-value">{predicted_demand:,.1f}</div>
      <div class="metric-note">kWh • demo estimate</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">GRID CAPACITY USED</div>
      <div class="metric-value">{load_percent:.1f}%</div>
      <div class="metric-note">of configured hourly capacity</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">SUGGESTED TARIFF</div>
      <div class="metric-value">₹{suggested_tariff:.2f}</div>
      <div class="metric-note">per kWh • illustrative rule</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">GRID STATUS</div>
      <div class="metric-value" style="color:{status_color};font-size:23px">
        {status}
      </div>
      <div class="metric-note">based on selected capacity</div>
    </div>""", unsafe_allow_html=True)

st.markdown("")

if load_percent >= 90:
    st.error("⚠️ High-load warning: estimated demand is at least 90% of the configured capacity.")
elif load_percent >= 65:
    st.warning("⚠️ Moderate load: monitor demand and consider load balancing.")
else:
    st.success("✓ Estimated demand is within the configured normal-load range.")

st.progress(min(max(int(load_percent), 0), 100))

# ---------- DEMAND GRAPH ----------
left, right = st.columns([1.7, 1])

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📈 Hourly demand profile")
    st.caption("Illustrative daily profile generated from your selected inputs.")

    hours = np.arange(24)
    profile = (
        0.45
        + 0.35 * np.exp(-((hours - 9) / 2.5) ** 2)
        + 0.60 * np.exp(-((hours - 19) / 3.0) ** 2)
    )

    hourly_demand = predicted_demand * profile / profile[hour]
    chart_data = pd.DataFrame({
        "Hour": hours,
        "Estimated demand (kWh)": hourly_demand
    }).set_index("Hour")

    st.line_chart(chart_data, height=300)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🌡️ Operating conditions")

    st.metric("Selected temperature", f"{temperature} °C")
    st.metric("Expected sessions", f"{sessions}")
    st.metric("Average session energy", f"{energy_per_session} kWh")
    st.metric("Configured capacity", f"{capacity} kWh/hour")

    st.caption(
        "Weather multipliers and peak-hour factors are illustrative "
        "assumptions, not learned relationships."
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- EXPLANATION ----------
st.markdown("")
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("🧠 How this prototype works")

st.markdown("""
1. You select the expected number of charging sessions and average energy.
2. The prototype adjusts the estimate using illustrative time and temperature factors.
3. It compares estimated energy demand with your configured capacity.
4. A simple rule suggests a tariff and displays a load warning.
""")

st.warning(
    "Research prototype: predictions currently use demo formulas, not a trained "
    "Machine Learning model or live grid data. The tariff is illustrative, "
    "not a real electricity price recommendation."
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    "<center><small>VoltIQ • Smart Grid EV Analytics • Mini Project</small></center>",
    unsafe_allow_html=True
)
