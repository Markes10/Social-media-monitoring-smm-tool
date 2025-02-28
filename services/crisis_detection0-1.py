import tweepy
import pandas as pd
import numpy as np
import sqlite3
from transformers import pipeline
from collections import deque, Counter
from datetime import datetime, timedelta
from sentiment_analysis import analyze_sentiment

# Twitter API credentials
TWITTER_API_KEY = "your_twitter_api_key"
TWITTER_API_SECRET = "your_twitter_api_secret"
TWITTER_ACCESS_TOKEN = "your_access_token"
TWITTER_ACCESS_SECRET = "your_access_secret"

# Authenticate Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Connect to database
conn = sqlite3.connect("smm_data.db")
cursor = conn.cursor()

# Queue to store sentiment trend
sentiment_trend = deque(maxlen=10)  # Store last 10 sentiment readings

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

def detect_crisis_twitter(brand, count=100, threshold=30):
    """Detect crisis based on Twitter sentiment spikes"""
    tweets = tweepy.Cursor(api.search_tweets, q=brand, lang="en", tweet_mode="extended").items(count)
    
    negative_count = 0
    for tweet in tweets:
        sentiment = analyze_sentiment(tweet.full_text)
        if sentiment == "Negative":
            negative_count += 1
    
    negative_percentage = (negative_count / count) * 100
    sentiment_trend.append(negative_percentage)
    
    # Check for sudden spike in negativity
    if len(sentiment_trend) > 5:
        avg_negative = np.mean(list(sentiment_trend)[-5:])
        if negative_percentage > avg_negative + threshold:
            return {"crisis_detected": True, "negative_percentage": negative_percentage}
    
    return {"crisis_detected": False, "negative_percentage": negative_percentage}

def detect_crisis_database(timeframe_hours=6, negative_threshold=30):
    """Detect crisis by analyzing sentiment spikes from stored mentions"""
    timeframe = datetime.utcnow() - timedelta(hours=timeframe_hours)
    
    cursor.execute("""
        SELECT sentiment FROM mentions 
        WHERE timestamp >= ?
    """, (timeframe.isoformat(),))
    
    sentiments = [row[0] for row in cursor.fetchall()]
    
    if not sentiments:
        return {"status": "No recent mentions"}
    
    sentiment_counts = Counter(sentiments)
    negative_count = sentiment_counts.get("Negative", 0)
    crisis_detected = negative_count > negative_threshold
    
    return {
        "crisis_detected": crisis_detected,
        "negative_mentions": negative_count,
        "total_mentions": sum(sentiment_counts.values()),
        "status": "Crisis detected 🚨" if crisis_detected else "No crisis"
    }

def detect_crisis(social_media_posts=None):
    """Detect a potential PR crisis by analyzing sentiment trends."""
    if social_media_posts is None:
        social_media_posts = [
            {"text": "I love this product! Amazing quality. #HappyCustomer", "timestamp": datetime.now() - timedelta(hours=2)},
            {"text": "Worst experience ever. Never buying again. #Disappointed", "timestamp": datetime.now() - timedelta(hours=1)},
            {"text": "This company is a scam! Avoid at all costs!", "timestamp": datetime.now()},
            {"text": "Great customer service! They really care about customers.", "timestamp": datetime.now() - timedelta(minutes=30)},
        ]
    
    crisis_alerts = []
    sentiments = [sentiment_analyzer(post["text"])[0] for post in social_media_posts]
    
    negative_count = 0
    for idx, sentiment in enumerate(sentiments):
        if sentiment["label"] == "NEGATIVE":
            negative_count += 1
            if sentiment["score"] > 0.8:
                crisis_alerts.append({
                    "text": social_media_posts[idx]["text"],
                    "timestamp": social_media_posts[idx]["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                    "alert_level": "HIGH",
                    "recommendation": "Immediate response required! Address customer concerns publicly and offer a resolution."
                })
    
    crisis_risk = (negative_count / len(social_media_posts)) * 100 if social_media_posts else 0
    response_strategy = "Monitor" if crisis_risk < 30 else "Alert Team & Respond Immediately"
    
    return {
        "crisis_detected": len(crisis_alerts) > 0,
        "negative_percentage": crisis_risk,
        "response_strategy": response_strategy,
        "alerts": crisis_alerts if crisis_alerts else "No crisis detected.",
        "details": sentiments
    }

# Example usage:
# print(detect_crisis_twitter("Tesla", 100))
# print(detect_crisis_database())
# posts = ["I hate this product!", "Worst customer service!", "Amazing experience!", "Terrible app!"]
# print(detect_crisis(posts))
