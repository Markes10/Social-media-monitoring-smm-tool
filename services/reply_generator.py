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
from models import SocialMediaPost
from database import get_db
import matplotlib.pyplot as plt
from jinja2 import Template

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

# Report Generation
def fetch_data():
    conn = sqlite3.connect("smm_data.db")
    query = "SELECT * FROM TrendingData"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def generate_visualizations(df):
    plt.figure(figsize=(10, 5))
    hashtags = df["hashtags"].str.split(", ").explode()
    hashtag_counts = hashtags.value_counts().head(5)
    hashtag_counts.plot(kind="bar", color="skyblue", title="Top Hashtags")
    plt.savefig("static/top_hashtags.png")
    plt.close()

    keywords = df["keywords"].str.split(", ").explode()
    keyword_counts = keywords.value_counts().head(5)
    keyword_counts.plot(kind="bar", color="lightcoral", title="Top Keywords")
    plt.savefig("static/top_keywords.png")
    plt.close()

def generate_report():
    df = fetch_data()
    if df.empty:
        return "No data available for reporting."
    generate_visualizations(df)
    template = Template("""
    <html>
    <head><title>Social Media Report</title></head>
    <body>
        <h1>📊 Social Media Monitoring Report</h1>
        <p><b>Total Posts Analyzed:</b> {{ total_posts }}</p>
        <h2>🔥 Top Trending Hashtags</h2>
        <img src="static/top_hashtags.png" width="500">
        <h2>💡 Top Keywords</h2>
        <img src="static/top_keywords.png" width="500">
    </body>
    </html>
    """)
    report_html = template.render(total_posts=len(df))
    with open("static/social_media_report.html", "w") as f:
        f.write(report_html)
    return "Report generated: static/social_media_report.html"

# Reply Generator
def generate_reply(comment):
    prompt = f"Reply politely and professionally to this comment: {comment}"
    response = reply_model(prompt, max_length=50, num_return_sequences=1)
    return response[0]["generated_text"]

# Example Usage
# print(generate_report())
# print(generate_reply("I love this product!"))