import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from database import SessionLocal
from models import Analytics

def predict_engagement(agency_id):
    db = SessionLocal()
    data = db.query(Analytics).filter(Analytics.agency_id == agency_id).all()
    
    if len(data) < 3:  
        return {"message": "Not enough data for prediction"}

    df = pd.DataFrame([(d.timestamp, d.engagement_rate) for d in data], columns=["timestamp", "engagement_rate"])
    df["timestamp"] = pd.to_datetime(df["timestamp"]).astype(int) / 10**9  

    X = df["timestamp"].values.reshape(-1, 1)
    y = df["engagement_rate"].values

    model = LinearRegression()
    model.fit(X, y)

    future_timestamp = np.array([[df["timestamp"].max() + 86400]])  # Predict for the next day
    prediction = model.predict(future_timestamp)

    return {"predicted_engagement_rate": round(prediction[0], 2)}
