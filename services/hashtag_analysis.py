import os
import random
import pandas as pd
import numpy as np
import tweepy
import snscrape.modules.twitter as sntwitter
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import nltk
import re
from bs4 import BeautifulSoup
from collections import Counter
from wordcloud import WordCloud
from transformers import pipeline
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
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
hashtag_analyzer = pipeline("fill-mask", model="distilroberta-base")
keyword_extractor = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
openai_api = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

nltk.download("stopwords")
STOPWORDS = set(nltk.corpus.stopwords.words("english"))

# Fetch Hashtag Posts
def fetch_hashtag_posts(hashtag):
    query = f"SELECT post FROM competitor_posts WHERE post LIKE '%{hashtag}%';"
    df = pd.read_sql_query(query, conn)
    return df["post"].tolist()

# Sentiment Analysis
def analyze_sentiment(posts):
    sentiments = [TextBlob(post).sentiment.polarity for post in posts]
    return sum(sentiments) / len(sentiments) if sentiments else 0

# Hashtag Engagement Analysis
def analyze_hashtag_engagement(hashtag, count=100):
    tweets = tweepy.Cursor(twitter_api.search_tweets, q=hashtag, lang="en", tweet_mode="extended").items(count)
    data, words = [], []
    for tweet in tweets:
        data.append({"likes": tweet.favorite_count, "retweets": tweet.retweet_count, "text": tweet.full_text})
        words.extend(re.sub(r"http\S+|@\S+", "", tweet.full_text).lower().split())
    words = [word for word in words if word not in STOPWORDS and len(word) > 2]
    word_freq = Counter(words)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("hashtag_wordcloud.png")
    return {"top_words": word_freq.most_common(10), "avg_likes": np.mean([d["likes"] for d in data]), "avg_retweets": np.mean([d["retweets"] for d in data])}

# Predict Future Trends
def predict_future_trends():
    future_trends = ["AI in marketing", "Blockchain social media", "Sustainable branding", "Hyper-personalized ads", "Social commerce growth"]
    return random.sample(future_trends, 3)

# Analyze Hashtags
def analyze_hashtags():
    trending = fetch_trending_hashtags()
    future_trends = predict_future_trends()
    recommended_hashtags = [hashtag_analyzer(f"#{t} is [MASK]", top_k=1)[0]["token_str"] for t in trending]
    return {"trending_hashtags": trending, "future_trends": future_trends, "recommended_hashtags": recommended_hashtags}

# Example Usage
# print(fetch_hashtag_posts("#AI"))
# print(analyze_hashtag_engagement("#AI"))
# print(predict_future_trends())
# print(analyze_hashtags())
