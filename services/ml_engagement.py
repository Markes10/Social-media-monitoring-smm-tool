import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sqlalchemy.orm import Session
from database import SessionLocal
from models import PostAnalytics

def train_engagement_model():
    """Trains a model to predict engagement scores for future posts."""
    
    db: Session = SessionLocal()
    data = db.query(PostAnalytics).all()

    if len(data) < 10:
        return None  # Not enough data to train

    df = pd.DataFrame([{
        "likes": p.likes,
        "shares": p.shares,
        "comments": p.comments,
        "impressions": p.impressions,
        "engagement_score": p.engagement_score
    } for p in data])

    X = df.drop(columns=["engagement_score"])
    y = df["engagement_score"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)

    return model
