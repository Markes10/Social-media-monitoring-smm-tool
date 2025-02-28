import os
import random
import pandas as pd
import numpy as np
import instaloader
import tweepy
import snscrape.modules.twitter as sntwitter
import sqlite3
import requests
import redis
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from transformers import pipeline
from datetime import datetime
from collections import Counter
from textblob import TextBlob
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, WebSocket, APIRouter, Depends
from celery import Celery
from celery.schedules import crontab
from jinja2 import Template
from openai import OpenAI
from routes import social_media, sentiment, realtime
from models import PostAnalytics

# Load environment variables
load_dotenv()

# Initialize FastAPI App
app = FastAPI(title="Social Media Monitoring API")

# Include routers
app.include_router(social_media.router, prefix="/api")
app.include_router(sentiment.router, prefix="/api")
app.include_router(realtime.router, prefix="/api")

# WebSocket Connections
active_connections = []

@app.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        active_connections.remove(websocket)

# Database Setup
DATABASE_URL = "sqlite:///smm_data.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis Configuration
redis_client = redis.Redis(host="localhost", port=6379, db=0)

# Celery Configuration
celery_app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")
celery_app.conf.beat_schedule = {
    "fetch_twitter_data_every_10s": {
        "task": "twitter_fetcher.fetch_twitter_data",
        "schedule": 10.0,
    }
}

@celery_app.task
def schedule_post(platform, content, post_time):
    return f"Post scheduled on {platform} at {post_time}: {content}"

@app.on_event("startup")
async def start_fetchers():
    pass

# ML Engagement Model
def train_engagement_model():
    db: Session = SessionLocal()
    data = db.query(PostAnalytics).all()

    if len(data) < 10:
        return None

    df = pd.DataFrame([{ "likes": p.likes, "shares": p.shares, "comments": p.comments, "impressions": p.impressions, "engagement_score": p.engagement_score } for p in data])
    X = df.drop(columns=["engagement_score"])
    y = df["engagement_score"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)
    return model

# Engagement Prediction
def predict_engagement(likes, shares, comments, impressions):
    model = train_engagement_model()
    if not model:
        return "Not enough data to predict engagement"
    features = np.array([[likes, shares, comments, impressions]])
    prediction = model.predict(features)
    return round(prediction[0], 2)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)