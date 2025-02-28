import os
import random
import pandas as pd
import numpy as np
import instaloader
import tweepy
import snscrape.modules.twitter as sntwitter
import sqlite3
import requests
import nltk
from dotenv import load_dotenv
from sklearn.preprocessing import MinMaxScaler
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
from collections import Counter
from textblob import TextBlob
from sqlalchemy.orm import Session
from models import SocialMediaPost
from database import get_db

# Load environment variables
load_dotenv()

# Initialize Sentiment Analysis
nltk.download("vader_lexicon")
sentiment_analyzer = pipeline("sentiment-analysis")
trend_analyzer = pipeline("text-classification", model="facebook/bart-large-mnli")
vader_analyzer = SentimentIntensityAnalyzer()
insta_loader = instaloader.Instaloader()

# Twitter API Authentication
auth = tweepy.OAuthHandler(os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_SECRET"))
twitter_api = tweepy.API(auth, wait_on_rate_limit=True)

# Function to analyze sentiment using multiple models
def analyze_sentiment(text):
    vader_score = vader_analyzer.polarity_scores(text)["compound"]
    bert_result = sentiment_analyzer(text)[0]
    
    if vader_score >= 0.05:
        vader_sentiment = "Positive"
    elif vader_score <= -0.05:
        vader_sentiment = "Negative"
    else:
        vader_sentiment = "Neutral"
    
    return {
        "text": text,
        "vader_sentiment": vader_sentiment,
        "bert_sentiment": bert_result["label"],
        "bert_confidence": round(bert_result["score"], 2)
    }

# Fetch Twitter Posts
def fetch_twitter_posts(keyword, count=100):
    tweets = tweepy.Cursor(twitter_api.search_tweets, q=keyword, lang="en", tweet_mode="extended").items(count)
    return [tweet.full_text for tweet in tweets]

# Sentiment Summary
def sentiment_summary(posts):
    sentiments = [analyze_sentiment(post) for post in posts]
    sentiment_counts = Counter(sent["bert_sentiment"] for sent in sentiments)
    
    crisis_level = "Low"
    if sentiment_counts.get("NEGATIVE", 0) > 5:
        crisis_level = "Medium"
    if sentiment_counts.get("NEGATIVE", 0) > 10:
        crisis_level = "High"
    
    return {
        "sentiment_summary": sentiment_counts,
        "crisis_level": crisis_level,
        "detailed_analysis": sentiments
    }

# Fetch Social Media Conversations
def fetch_social_posts_api(platform, keyword):
    if platform.lower() == "twitter":
        url = f"https://api.twitter.com/2/tweets/search/recent?query={keyword}"
        headers = {"Authorization": f"Bearer {os.getenv('TWITTER_API_KEY')}"}
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": "Failed to fetch data"}
        
        tweets = response.json().get("data", [])
        return [tweet["text"] for tweet in tweets]
    return {"error": "Platform not supported"}

# Example Usage:
# tweets = fetch_twitter_posts("Tesla", 50)
# print(sentiment_summary(tweets))
