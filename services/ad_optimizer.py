import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Sample dataset (ad spend, engagement, CTR, conversion rate)
data = {
    "ad_spend": [100, 200, 300, 400, 500],
    "click_through_rate": [2.5, 3.2, 4.1, 4.8, 5.5],
    "conversion_rate": [1.2, 1.8, 2.4, 2.9, 3.3],
    "roi": [1.5, 2.0, 2.7, 3.1, 3.5]  # Target: ROI (Return on Investment)
}

df = pd.DataFrame(data)

# Train AI model
X = df.drop(columns=["roi"])
y = df["roi"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = xgb.XGBRegressor(objective="reg:squarederror")
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Model MAE: {mae}")

def optimize_ad_budget(ad_spend, ctr, conversion_rate):
    """Predict the best budget allocation using AI."""
    input_data = pd.DataFrame([[ad_spend, ctr, conversion_rate]], columns=X.columns)
    return model.predict(input_data)[0]

# Example usage:
# print(optimize_ad_budget(600, 6.0, 3.8))
