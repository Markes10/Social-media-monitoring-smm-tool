import tweepy
import os
from database import SessionLocal
from models import SocialMediaPost

# Twitter API Keys (Replace with your own)
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_SECRET = "your_access_secret"

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def fetch_tweets(keyword: str):
    tweets = api.search_tweets(q=keyword, count=10, lang="en")
    db = SessionLocal()

    for tweet in tweets:
        new_post = SocialMediaPost(
            platform="Twitter",
            username=tweet.user.screen_name,
            content=tweet.text,
            sentiment="Pending"
        )
        db.add(new_post)
    
    db.commit()
    db.close()
