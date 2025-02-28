import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Simulated ad campaign data (real data should be pulled from campaign logs)
data = {
    "budget": [500, 1000, 2000, 3000, 5000, 7000, 10000, 15000],
    "target_audience": [10000, 20000, 50000, 75000, 100000, 150000, 200000, 300000],
    "past_ctr": [2.1, 2.5, 3.2, 3.5, 4.1, 4.5, 5.2, 5.8],
    "conversions": [50, 100, 200, 300, 500, 700, 1000, 1500],
}

df = pd.DataFrame(data)

# Features and target
X = df[["budget", "target_audience", "past_ctr"]]
y = df["conversions"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a machine learning model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Model MAE: {mae}")

# Save the model
joblib.dump(model, "ad_performance_model.pkl")
