import os
import random
import pandas as pd
import numpy as np
import tweepy
import snscrape.modules.twitter as sntwitter
import requests
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
from transformers import pipeline
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from collections import Counter
from datetime import datetime
from textblob import TextBlob
from openai import OpenAI

# Load environment variables
load_dotenv()

# Twitter API Setup
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
twitter_api = tweepy.API(auth)

# Database Setup
DATABASE_URL = "sqlite:///smm_data.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
conn = sqlite3.connect("smm_data.db")
cursor = conn.cursor()

# AI Models
sentiment_analyzer = pipeline("sentiment-analysis")
openai_api = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Competitor Tweet Scraping
def scrape_competitor_tweets(competitor, limit=100):
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(f"{competitor} -filter:retweets").get_items():
        if len(tweets) >= limit:
            break
        sentiment = sentiment_analyzer(tweet.content)[0]["label"]
        timestamp = datetime.utcnow().isoformat()
        cursor.execute("INSERT INTO competitor_sentiment (timestamp, competitor, sentiment, tweet) VALUES (?, ?, ?, ?)",
                       (timestamp, competitor, sentiment, tweet.content))
        conn.commit()
        tweets.append({"timestamp": timestamp, "competitor": competitor, "sentiment": sentiment, "tweet": tweet.content})
    return tweets

# Web Scraping Competitor Posts
def fetch_competitor_posts(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}
    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.find_all("div", class_="tweet-text")
    data = []
    for post in posts[:10]:
        text = post.get_text()
        engagement = len(text) * 2
        data.append({"post": text, "engagement": engagement})
    return data

# Store Competitor Data
def store_competitor_data(competitor, posts):
    for post in posts:
        cursor.execute("INSERT INTO competitor_posts VALUES (?, ?)", (competitor, post))
    conn.commit()

# Analyze Trending Content
def analyze_trending_content(posts_data):
    df = pd.DataFrame(posts_data)
    top_posts = df.nlargest(3, "engagement")["post"].tolist()
    return {"trending_posts": top_posts}

# Example Usage
# print(scrape_competitor_tweets("CompetitorX", limit=10))
# posts = fetch_competitor_posts("https://twitter.com/CompetitorHandle")
# store_competitor_data("CompetitorX", posts)
# print(analyze_trending_content(posts))
