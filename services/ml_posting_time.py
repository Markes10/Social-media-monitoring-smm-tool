import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy.orm import Session
from database import SessionLocal
from models import PostAnalytics

def train_posting_time_model():
    """Trains a model to recommend the best posting time."""
    
    db: Session = SessionLocal()
    data = db.query(PostAnalytics).all()

    if len(data) < 10:
        return None  # Not enough data

    df = pd.DataFrame([{
        "hour": p.created_at.hour,
        "engagement_score": p.engagement_score
    } for p in data])

    X = df[["hour"]]
    y = df["engagement_score"]

    model = LinearRegression()
    model.fit(X, y)

    return model

def recommend_best_posting_time():
    """Predicts the best posting time based on engagement trends."""
    
    model = train_posting_time_model()
    if not model:
        return "Not enough data to predict best posting time"

    hours = np.array(range(24)).reshape(-1, 1)
    predictions = model.predict(hours)
    best_hour = np.argmax(predictions)

    return f"Best posting time: {best_hour}:00"
