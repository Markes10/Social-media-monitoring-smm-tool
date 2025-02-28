import os
import asyncio
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
from routes import social_media, sentiment, realtime

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

# Initialize Sentiment Analysis
sentiment_analyzer = pipeline("sentiment-analysis")
trend_analyzer = pipeline("text-classification", model="facebook/bart-large-mnli")
reply_model = pipeline("text-generation", model="gpt2")
insta_loader = instaloader.Instaloader()

# Twitter API Authentication
auth = tweepy.OAuthHandler(os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_SECRET"))
twitter_api = tweepy.API(auth, wait_on_rate_limit=True)

# SQLite Database
conn = sqlite3.connect("smm_data.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS social_media_posts (post_id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, sentiment_score REAL, platform TEXT, timestamp TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS TrendingData (id INTEGER PRIMARY KEY AUTOINCREMENT, hashtags TEXT, keywords TEXT)")
conn.commit()

# PostgreSQL Database
DATABASE_URL = "postgresql://username:password@localhost/smm_db"
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
    asyncio.create_task(fetch_twitter_data())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)