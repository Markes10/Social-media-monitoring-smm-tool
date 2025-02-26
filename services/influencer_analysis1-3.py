import os
import random
import pandas as pd
import numpy as np
import instaloader
import tweepy
from dotenv import load_dotenv
from sklearn.preprocessing import MinMaxScaler
from transformers import pipeline

# Load environment variables
load_dotenv()

# Initialize sentiment analysis
sentiment_analyzer = pipeline("sentiment-analysis")

# Initialize Instaloader
insta_loader = instaloader.Instaloader()

# Twitter API authentication
auth = tweepy.OAuthHandler(os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_SECRET"))
twitter_api = tweepy.API(auth)

def fetch_instagram_influencer(username):
    """Fetch Instagram influencer stats."""
    profile = instaloader.Profile.from_username(insta_loader.context, username)
    return {
        "followers": profile.followers,
        "following": profile.followees,
        "posts": profile.mediacount,
        "engagement_rate": round((profile.followers / profile.mediacount) * 100, 2)
    }

def fetch_twitter_influencer(handle):
    """Fetch Twitter influencer stats."""
    user = twitter_api.get_user(screen_name=handle)
    return {
        "followers": user.followers_count,
        "tweets": user.statuses_count,
        "likes": user.favourites_count,
        "engagement_rate": round((user.followers_count / max(user.statuses_count, 1)) * 100, 2)
    }

def fetch_top_influencers(hashtag, count=10):
    """Fetch top influencers based on engagement with a hashtag."""
    tweets = tweepy.Cursor(twitter_api.search_tweets, q=f"#{hashtag}", lang="en", tweet_mode="extended").items(count)
    influencer_data = []
    
    for tweet in tweets:
        influencer_data.append({
            "username": tweet.user.screen_name,
            "followers": tweet.user.followers_count,
            "likes": tweet.favorite_count,
            "retweets": tweet.retweet_count,
            "engagement": tweet.favorite_count + tweet.retweet_count
        })
    
    influencers_df = pd.DataFrame(influencer_data)
    top_influencers = influencers_df.sort_values(by="engagement", ascending=False).head(5)
    return top_influencers.to_dict(orient="records")

def analyze_influencer_sentiment(influencer):
    """Analyze the sentiment of an influencer's audience comments."""
    sentiments = [sentiment_analyzer(comment)[0]["label"] for comment in influencer["comments"]]
    return {
        "positive": sentiments.count("POSITIVE"),
        "neutral": sentiments.count("NEUTRAL"),
        "negative": sentiments.count("NEGATIVE")
    }

def get_top_influencers():
    """Get AI-powered influencer recommendations."""
    influencers = [
        {"name": "JohnDoe_Influencer", "followers": 150000, "engagement_rate": 4.2, "fake_followers": 5, "comments": ["Great post!", "Love this!", "Amazing!"]},
        {"name": "JaneSmith_Blogger", "followers": 300000, "engagement_rate": 2.1, "fake_followers": 20, "comments": ["So inspiring!", "Wow!", "Great insights."]},
        {"name": "MarkTech_Guru", "followers": 50000, "engagement_rate": 5.8, "fake_followers": 2, "comments": ["Very informative!", "Awesome content!", "Love the details!"]},
    ]
    influencer_data = []
    
    for influencer in influencers:
        sentiment_analysis = analyze_influencer_sentiment(influencer)
        influencer_data.append({
            "name": influencer["name"],
            "followers": influencer["followers"],
            "engagement_rate": influencer["engagement_rate"],
            "fake_followers": influencer["fake_followers"],
            "sentiment_analysis": sentiment_analysis
        })
    
    influencer_data.sort(key=lambda x: (x["engagement_rate"], -x["fake_followers"]), reverse=True)
    return influencer_data

def recommend_influencer():
    """Recommend the best influencer based on engagement and authenticity."""
    data = {
        "influencer": ["@tech_guru", "@fitness_queen", "@travel_nomad", "@foodie_chef", "@gaming_pro"],
        "followers": [500000, 800000, 300000, 600000, 700000],
        "engagement_rate": [4.5, 6.8, 3.2, 5.0, 6.1],
        "authenticity_score": [90, 85, 80, 88, 92]
    }
    df = pd.DataFrame(data)
    df["score"] = (df["followers"] * 0.4) + (df["engagement_rate"] * 2000 * 0.4) + (df["authenticity_score"] * 0.2)
    scaler = MinMaxScaler()
    df["score"] = scaler.fit_transform(df["score"].values.reshape(-1, 1))
    best_influencer = df.iloc[df["score"].idxmax()]
    
    return {
        "recommended_influencer": best_influencer["influencer"],
        "followers": best_influencer["followers"],
        "engagement_rate": best_influencer["engagement_rate"],
        "authenticity_score": best_influencer["authenticity_score"],
        "recommendation": f"Partner with {best_influencer['influencer']} for high engagement and authenticity."
    }

# Example usage:
# print(fetch_instagram_influencer("cristiano"))
# print(fetch_twitter_influencer("elonmusk"))
# print(fetch_top_influencers("AI", count=50))
# print(get_top_influencers())
# print(recommend_influencer())
