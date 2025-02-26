import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy.orm import Session
from database import SessionLocal
from models import AdPerformance

def train_ad_performance_model():
    """Trains an AI model to predict ad performance."""
    
    db: Session = SessionLocal()
    data = db.query(AdPerformance).all()

    if len(data) < 10:
        return None  # Not enough data

    df = pd.DataFrame([{
        "impressions": ad.impressions,
        "clicks": ad.clicks,
        "conversions": ad.conversions,
        "engagement_score": ad.engagement_score
    } for ad in data])

    X = df[["impressions", "clicks", "conversions"]]
    y = df["engagement_score"]

    model = LinearRegression()
    model.fit(X, y)

    return model

def predict_best_ad(impressions, clicks, conversions):
    """Predicts engagement score for a given ad."""
    
    model = train_ad_performance_model()
    if not model:
        return "Not enough data to predict ad performance."

    predicted_score = model.predict(np.array([[impressions, clicks, conversions]]))
    return round(predicted_score[0], 2)
