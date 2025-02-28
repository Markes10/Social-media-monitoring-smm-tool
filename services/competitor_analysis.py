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

# Fetch Competitor Mentions
def get_competitor_data(competitor):
    query = "SELECT platform, mentions, engagement, sentiment FROM competitor_tracking WHERE competitor_name = ?"
    cursor.execute(query, (competitor,))
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["Platform", "Mentions", "Engagement", "Sentiment"])
    return df.to_dict(orient="records")

# Extract Hashtags
def extract_hashtags(text):
    return re.findall(r"#\w+", text)

# Analyze Hashtag Trends
def analyze_trends():
    query = "SELECT post FROM competitor_posts"
    df = pd.read_sql_query(query, conn)
    hashtags = [tag for post in df["post"] for tag in extract_hashtags(post)]
    top_trends = Counter(hashtags).most_common(10)
    return top_trends

# Analyze Competitor Performance
def compare_with_competitor(agency_id):
    db: Session = SessionLocal()
    agency_posts = db.query(PostAnalytics).filter(PostAnalytics.agency_id == agency_id).all()
    competitors = db.query(CompetitorAnalysis).filter(CompetitorAnalysis.agency_id == agency_id).all()

    insights = []
    if not agency_posts or not competitors:
        return "Not enough data to compare."

    agency_avg = np.mean([post.engagement_score for post in agency_posts])
    for competitor in competitors:
        engagement_diff = agency_avg - competitor.avg_engagement
        advice = "Increase engagement by posting interactive content." if engagement_diff > 0 else "Adapt strategy based on competitor analysis."
        insights.append({
            "competitor": competitor.competitor_name,
            "your_engagement": round(agency_avg, 2),
            "competitor_engagement": competitor.avg_engagement,
            "advice": advice
        })
    db.close()
    return insights

# Fetch Competitor Metrics
def fetch_competitor_metrics(competitor_handles, count=50):
    competitor_data = []
    for handle in competitor_handles:
        tweets = tweepy.Cursor(twitter_api.user_timeline, screen_name=handle, tweet_mode="extended").items(count)
        likes, retweets = 0, 0
        for tweet in tweets:
            likes += tweet.favorite_count
            retweets += tweet.retweet_count
        competitor_data.append({
            "competitor": handle,
            "total_likes": likes,
            "total_retweets": retweets,
            "engagement_score": likes + (2 * retweets)
        })
    df = pd.DataFrame(competitor_data)
    sns.barplot(x="competitor", y="engagement_score", data=df, palette="coolwarm")
    plt.title("Competitor Engagement Score")
    plt.savefig("competitor_analysis.png")
    return df.to_dict(orient="records")

# AI-Based Competitor Insights
def analyze_competitor_trends(df):
    prompt = f"""
    Here is social media data from competitors:
    {df.to_string(index=False)}

    Identify trending topics, content types, and strategies to improve engagement.
    """
    response = openai_api.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}], max_tokens=200)
    return response['choices'][0]['message']['content'].strip()

# Example Usage
# print(get_competitor_data("BrandX"))
# print(fetch_competitor_metrics(["@brandA", "@brandB"]))
# print(analyze_competitor_trends(fetch_competitor_data()))
