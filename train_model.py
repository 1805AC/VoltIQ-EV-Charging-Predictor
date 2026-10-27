
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import pickle
import os

# 1. Load the dataset
data = pd.read_csv("data/ev_charging_small_dataset.csv")

# 2. Select input features
X = data[["hour", "temperature_c", "charging_sessions"]]

# 3. Select the value we want to predict
y = data["energy_demand_kwh"]

# 4. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Train the regression model
model = LinearRegression()
model.fit(X_train, y_train)

# 6. Test the model
predictions = model.predict(X_test)

print("Model training completed!")
mae = round(mean_absolute_error(y_test, predictions), 2)
r2 = round(r2_score(y_test, predictions), 2)

print("Mean Absolute Error:", mae)
print("R2 Score:", r2)

import json

with open("models/model_metrics.json", "w") as file:
    json.dump({"mae": mae, "r2_score": r2}, file, indent=4)

print("Model metrics saved successfully!")
# 7. Save the trained model
os.makedirs("models", exist_ok=True)

with open("models/ev_demand_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model saved to models/ev_demand_model.pkl")
