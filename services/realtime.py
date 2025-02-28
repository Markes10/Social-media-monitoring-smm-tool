import numpy as np
import pandas as pd
import asyncio
from sklearn.linear_model import LinearRegression
from sqlalchemy.sql import func
from database import SessionLocal
from models import Analytics, SocialMediaPost
from redis import Redis

redis_client = Redis(host='localhost', port=6379, db=0)

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

def best_posting_time(agency_id):
    """Finds the best time to post based on engagement trends."""
    db = SessionLocal()
    posts = db.query(
        func.strftime('%H', SocialMediaPost.timestamp).label("hour"),
        func.avg(SocialMediaPost.engagement_score).label("avg_engagement")
    ).filter(SocialMediaPost.agency_id == agency_id).group_by("hour").all()

    if not posts:
        return {"message": "Not enough data to determine best posting time"}

    best_hour = max(posts, key=lambda x: x.avg_engagement)
    
    return {"best_posting_hour": f"{best_hour.hour}:00"}

def check_negative_sentiment(db: Session):
    # Try fetching from Redis first
    cached_count = redis_client.get("negative_count")
    
    if cached_count:
        negative_count = int(cached_count)
    else:
        # If not cached, fetch from DB and store in Redis
        negative_count = db.query(SocialMediaPost).filter(SocialMediaPost.sentiment == "negative").count()
        redis_client.setex("negative_count", 60, negative_count)  # Cache for 1 minute

    if negative_count > 5:
        alert_message = f"🚨 ALERT: {negative_count} negative posts detected!"
        asyncio.create_task(broadcast_message(alert_message))
