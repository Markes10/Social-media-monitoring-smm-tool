from celery_config import celery_app
import tweepy
from database import SessionLocal
from models import SocialMediaPost
from routes.realtime import broadcast_message

BEARER_TOKEN = "YOUR_TWITTER_BEARER_TOKEN"
client = tweepy.Client(bearer_token=BEARER_TOKEN)

@celery_app.task
def fetch_twitter_data():
    db = SessionLocal()
    tweets = client.search_recent_tweets(query="AI OR climate -is:retweet", max_results=10, tweet_fields=["text"])

    for tweet in tweets.data:
        post = SocialMediaPost(content=tweet.text, sentiment="neutral")
        db.add(post)
        broadcast_message(f"🐦 New Tweet: {tweet.text}")

    db.commit()
