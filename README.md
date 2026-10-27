
# VoltIQ – EV Charging Demand Predictor
🚀 **Live Demo:** [Open VoltIQ Dashboard](https://voltiq-ev-charging-predictor-mazwff9nsrb267g3nkbiwa.streamlit.app/)

## About the Project
VoltIQ is a Machine Learning mini-project that predicts electric vehicle (EV) charging energy demand based on the hour, temperature, and number of charging sessions.

The project uses a Linear Regression model and provides an interactive dashboard built with Streamlit.

## Features
- Predicts EV charging energy demand in kWh.
- Accepts hour, temperature, and charging session inputs.
- Displays demand-based charging prices.
- Shows grid load status using demo rules.
- Estimates potential revenue.
- Displays actual vs. predicted demand in a chart.
- Calculates model evaluation metrics.
- Saves prediction history.
- Allows users to view and download prediction history.

## Technologies Used
- Python
- Machine Learning
- Scikit-learn
- Pandas
- NumPy
- Streamlit
- Matplotlib

## Machine Learning Algorithm
**Linear Regression**

### Input Features
- Hour
- Temperature (°C)
- Number of charging sessions

### Output
- Predicted Energy Demand (kWh)

## Project Structure

```text
EV_Charging_Predictor/
├── app.py
├── train_model.py
├── requirements.txt
├── README.md
├── data/
│   └── ev_charging_small_dataset.csv
├── models/
│   ├── ev_demand_model.pkl
│   └── model_metrics.json
└── prediction_history.csv
```

## How to Run the Project

### Step 1: Install Dependencies

Open the terminal in VS Code and run:

```bash
pip install -r requirements.txt
```

### Step 2: Start the Streamlit Application

Run:

```bash
streamlit run app.py
```

### Step 3: Use the Dashboard

1. Enter the hour.
2. Enter the temperature.
3. Enter the number of charging sessions.
4. Generate the energy demand prediction.
5. View the estimated price, grid load status, and revenue.
6. Save the prediction and download the history if required.

## Dataset
This project uses a small sample dataset created for educational and demonstration purposes.

The dataset is not real-time EV charging data.

## Limitations
- The model uses a small sample dataset.
- Predictions may not represent actual charging demand.
- Charging prices and grid load status are based on demonstration rules.
- Estimated revenue is a calculation, not actual business revenue.

## Future Scope
- Use a larger real-world EV charging dataset.
- Integrate live weather information.
- Add real-time charging station data.
- Improve prediction accuracy.
- Deploy the application online.

## Conclusion
VoltIQ demonstrates how Machine Learning can be used to estimate EV charging energy demand through an interactive Streamlit dashboard.
