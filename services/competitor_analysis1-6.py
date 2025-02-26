import requests
import random
import pandas as pd
import numpy as np
import tweepy
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import pipeline
from sqlalchemy.orm import Session
from database import SessionLocal
from models import CompetitorAnalysis, PostAnalytics
from sklearn.preprocessing import MinMaxScaler
import os

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# Twitter API credentials
TWITTER_API_KEY = "your_twitter_api_key"
TWITTER_API_SECRET = "your_twitter_api_secret"
TWITTER_ACCESS_TOKEN = "your_access_token"
TWITTER_ACCESS_SECRET = "your_access_secret"

# Authenticate Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)

def compare_with_competitor(agency_id):
    db: Session = SessionLocal()
    agency_posts = db.query(PostAnalytics).filter(PostAnalytics.agency_id == agency_id).all()
    competitors = db.query(CompetitorAnalysis).filter(CompetitorAnalysis.agency_id == agency_id).all()

    if not agency_posts or not competitors:
        return "Not enough data to compare."

    agency_avg = np.mean([post.engagement_score for post in agency_posts])
    insights = []
    for competitor in competitors:
        engagement_diff = agency_avg - competitor.avg_engagement
        trend_analysis = f"Competitor trending topics: {competitor.trending_topics}"
        advice = "Increase engagement by posting more interactive content."
        if engagement_diff < 0:
            advice = "Your competitor has higher engagement. Analyze their strategy and adapt."
        insights.append({
            "competitor": competitor.competitor_name,
            "your_engagement": round(agency_avg, 2),
            "competitor_engagement": competitor.avg_engagement,
            "insight": trend_analysis,
            "advice": advice
        })
    db.close()
    return insights

def fetch_competitor_data(competitor_handle):
    api_url = f"https://api.twitter.com/2/users/by/username/{competitor_handle}?user.fields=public_metrics"
    headers = {"Authorization": f"Bearer {os.getenv('TWITTER_BEARER_TOKEN')}"}
    response = requests.get(api_url, headers=headers)
    return response.json()

def fetch_competitor_metrics(competitor_handles, count=50):
    competitor_data = []
    for handle in competitor_handles:
        tweets = tweepy.Cursor(api.user_timeline, screen_name=handle, tweet_mode="extended").items(count)
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
    plt.figure(figsize=(8, 5))
    sns.barplot(x="competitor", y="engagement_score", data=df, palette="coolwarm")
    plt.title("Competitor Engagement Score")
    plt.ylabel("Engagement Score")
    plt.xlabel("Competitor")
    plt.xticks(rotation=45)
    plt.savefig("competitor_analysis.png")
    return df.to_dict(orient="records")

def analyze_competitor_performance():
    competitors = ["@brandA", "@brandB", "@brandC"]
    data = []
    for competitor in competitors:
        engagement = random.randint(1000, 10000)
        sentiment = sentiment_analyzer(random.choice([
            "I love this brand!", "Not happy with the product.", "Best service ever!", "Terrible experience, never again."
        ]))[0]
        data.append({
            "competitor": competitor,
            "engagement": engagement,
            "sentiment": sentiment["label"],
            "sentiment_score": round(sentiment["score"], 2)
        })
    df = pd.DataFrame(data)
    avg_engagement = df["engagement"].mean()
    avg_sentiment_score = df["sentiment_score"].mean()
    return {
        "competitor_data": data,
        "benchmark": {"average_engagement": avg_engagement, "average_sentiment_score": avg_sentiment_score}
    }

def get_competitor_analysis():
    competitors = [
        {"name": "BrandX", "posts": ["Amazing new product!", "50% off sale now!", "We love our customers!"], "hashtags": ["#BestDeals", "#NewLaunch"], "engagement": 4.2},
        {"name": "BrandY", "posts": ["Eco-friendly products available!", "Customer spotlight: Meet Sarah!", "Join our giveaway!"], "hashtags": ["#Sustainable", "#Giveaway"], "engagement": 3.8},
        {"name": "BrandZ", "posts": ["Our biggest discount yet!", "Upgrade your style!", "Tag a friend for a chance to win!"], "hashtags": ["#Fashion", "#WinBig"], "engagement": 4.5},
    ]
    competitor_data = []
    for competitor in competitors:
        sentiment_analysis = analyze_competitor_sentiment(competitor)
        competitor_data.append({
            "name": competitor["name"],
            "engagement": competitor["engagement"],
            "top_hashtags": competitor["hashtags"],
            "sentiment_analysis": sentiment_analysis
        })
    competitor_data.sort(key=lambda x: x["engagement"], reverse=True)
    return competitor_data