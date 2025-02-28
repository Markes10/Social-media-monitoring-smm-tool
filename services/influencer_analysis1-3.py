import os
import random
import pandas as pd
import numpy as np
import instaloader
import tweepy
import snscrape.modules.twitter as sntwitter
import sqlite3
from dotenv import load_dotenv
from sklearn.preprocessing import MinMaxScaler
from transformers import pipeline
from datetime import datetime
from sentiment_analysis import analyze_sentiment

# Load environment variables
load_dotenv()

# Initialize Sentiment Analysis
sentiment_analyzer = pipeline("sentiment-analysis")
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

# Top Influencers
def get_top_influencers():
    influencers = ["JohnDoe", "JaneSmith", "TechGuru"]
    return [{"name": inf, "engagement_rate": random.uniform(2, 10)} for inf in influencers]

# Recommendation
def recommend_influencer():
    data = pd.DataFrame({"name": ["@tech_guru", "@fitness_queen"], "followers": [500000, 800000], "engagement_rate": [4.5, 6.8], "authenticity_score": [90, 85]})
    data["score"] = (data["followers"] * 0.4) + (data["engagement_rate"] * 2000 * 0.4) + (data["authenticity_score"] * 0.2)
    scaler = MinMaxScaler()
    data["score"] = scaler.fit_transform(data["score"].values.reshape(-1, 1))
    best = data.iloc[data["score"].idxmax()]
    return {"influencer": best["name"], "score": best["score"]}

# Example Usage
# print(fetch_instagram_influencer("cristiano"))
# print(fetch_twitter_influencer("elonmusk"))
# print(get_influencers("Tesla"))
# print(analyze_influencer("elonmusk", 10))
# print(get_top_influencers())
# print(recommend_influencer())
