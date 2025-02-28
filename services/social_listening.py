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
from sentiment_analysis import analyze_sentiment

# Load environment variables
load_dotenv()

# Initialize Sentiment Analysis
sentiment_analyzer = pipeline("sentiment-analysis")
trend_analyzer = pipeline("text-classification", model="facebook/bart-large-mnli")
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
conn.commit()

# Instagram Fetch
def fetch_instagram_influencer(username):
    profile = instaloader.Profile.from_username(insta_loader.context, username)
    return {
        "followers": profile.followers,
        "posts": profile.mediacount,
        "engagement_rate": round((profile.followers / profile.mediacount) * 100, 2)
    }

# Twitter Fetch
def fetch_twitter_influencer(handle):
    user = twitter_api.get_user(screen_name=handle)
    return {
        "followers": user.followers_count,
        "tweets": user.statuses_count,
        "engagement_rate": round((user.followers_count / max(user.statuses_count, 1)) * 100, 2)
    }

# Detect Influencers
def get_influencers(brand, count=100):
    tweets = tweepy.Cursor(twitter_api.search_tweets, q=brand, lang="en", tweet_mode="extended").items(count)
    influencer_data = {}
    
    for tweet in tweets:
        user = tweet.user.screen_name
        engagement = tweet.favorite_count + (tweet.retweet_count * 2)
        followers = tweet.user.followers_count
        influencer_data[user] = {"followers": followers, "engagement": influencer_data.get(user, {}).get("engagement", 0) + engagement}

    sorted_influencers = sorted(influencer_data.items(), key=lambda x: (x[1]["engagement"], x[1]["followers"]), reverse=True)
    return [{"username": user, "followers": data["followers"], "engagement": data["engagement"]} for user, data in sorted_influencers[:10]]

# Sentiment Scraper
def analyze_influencer(influencer, limit=100):
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(f"@{influencer} -filter:retweets").get_items():
        if len(tweets) >= limit:
            break
        sentiment = analyze_sentiment(tweet.content)
        cursor.execute("INSERT INTO influencer_sentiment (timestamp, influencer, sentiment, tweet) VALUES (?, ?, ?, ?)",
                       (datetime.utcnow().isoformat(), influencer, sentiment, tweet.content))
        conn.commit()
        tweets.append({"timestamp": datetime.utcnow().isoformat(), "influencer": influencer, "sentiment": sentiment, "tweet": tweet.content})
    return tweets

# Brand Mentions
def get_brand_mentions(brand_name):
    query = """
        SELECT post_id, content, sentiment_score, platform, timestamp
        FROM social_media_posts
        WHERE content LIKE ?
        ORDER BY timestamp DESC
        LIMIT 10
    """
    cursor.execute(query, (f"%{brand_name}%",))
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["Post ID", "Content", "Sentiment Score", "Platform", "Timestamp"])
    return df.to_dict(orient="records")

# Social Conversations
def fetch_social_conversations(platform, keyword):
    if platform.lower() == "twitter":
        url = f"https://api.twitter.com/2/tweets/search/recent?query={keyword}"
        headers = {"Authorization": f"Bearer {os.getenv('TWITTER_API_KEY')}"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": "Failed to fetch data"}
        return [tweet["text"] for tweet in response.json().get("data", [])]
    return {"error": "Platform not supported"}

# Trend Detection
def detect_trends(posts):
    words = [word.lower() for post in posts for word in post.split()]
    common_words = Counter(words).most_common(10)
    trend_predictions = trend_analyzer([word[0] for word in common_words])
    return {"trending_topics": [{"keyword": word[0], "trend_score": pred["score"]} for word, pred in zip(common_words, trend_predictions)]}

# Example Usage
# print(fetch_instagram_influencer("cristiano"))
# print(get_brand_mentions("Nike"))
# print(detect_trends(fetch_social_conversations("twitter", "AI technology")))
