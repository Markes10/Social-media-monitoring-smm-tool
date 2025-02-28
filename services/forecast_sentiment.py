import pandas as pd
import sqlite3
from prophet import Prophet

def forecast_sentiment(topic):
    """Predict future sentiment trends using Facebook's Prophet"""
    
    # Load historical sentiment data
    conn = sqlite3.connect("smm_data.db")
    df = pd.read_sql(f"SELECT timestamp, sentiment FROM sentiment_history WHERE topic='{topic}'", conn)
    
    # Convert sentiment labels to numeric values
    sentiment_map = {"Positive": 1, "Neutral": 0, "Negative": -1}
    df["y"] = df["sentiment"].map(sentiment_map)
    df["ds"] = pd.to_datetime(df["timestamp"])
    
    # Train forecasting model
    model = Prophet()
    model.fit(df[["ds", "y"]])
    
    # Predict next 30 days
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(10).to_dict(orient="records")

# Example usage:
# print(forecast_sentiment("ProductX"))
