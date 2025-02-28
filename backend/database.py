import os
import random
import pandas as pd
import numpy as np
import instaloader
import tweepy
import snscrape.modules.twitter as sntwitter
import sqlite3
import requests
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
import redis
import matplotlib.pyplot as plt
from jinja2 import Template
from celery import Celery
from celery.schedules import crontab

# Load environment variables
load_dotenv()

# Initialize Sentiment Analysis
sentiment_analyzer = pipeline("sentiment-analysis")
trend_analyzer = pipeline("text-classification", model="facebook/bart-large-mnli")
reply_model = pipeline("text-generation", model="gpt2")
insta_loader = instaloader.Instaloader()

# Twitter API Authentication
auth = tweepy.OAuthHandler(os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_SECRET"))
twitter_api = tweepy.API(auth, wait_on_rate_limit=True)

# SQLite Database Connection
conn = sqlite3.connect("smm_data.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS influencer_sentiment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    influencer TEXT,
    sentiment TEXT,
    tweet TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS social_media_posts (
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    sentiment_score REAL,
    platform TEXT,
    timestamp TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS TrendingData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hashtags TEXT,
    keywords TEXT
)
""")
conn.commit()

# PostgreSQL Database Configuration
DATABASE_URL = "postgresql://username:password@localhost/smm_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Redis Configuration
redis_client = redis.Redis(host="localhost", port=6379, db=0)

# Celery Configuration
celery_app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")
celery_app.conf.beat_schedule = {
    "fetch_twitter_data_every_10s": {
        "task": "twitter_fetcher.fetch_twitter_data",
        "schedule": 10.0,
    },
    "fetch_facebook_data_every_10s": {
        "task": "facebook_fetcher.fetch_facebook_data",
        "schedule": 10.0,
    },
}

@celery_app.task
def schedule_post(platform, content, post_time):
    return f"Post scheduled on {platform} at {post_time}: {content}"

# Example Usage
# print(generate_report())
# print(generate_reply("I love this product!"))
