import tweepy
import asyncio
from celery_config import celery_app
from database import SessionLocal
from models import SocialMediaPost
from routes.realtime import broadcast_message

# Twitter API Credentials
BEARER_TOKEN = "YOUR_TWITTER_BEARER_TOKEN"
client = tweepy.Client(bearer_token=BEARER_TOKEN)

def fetch_twitter_data_sync():
    """Fetch Twitter data synchronously using Celery."""
    db = SessionLocal()
    tweets = client.search_recent_tweets(query="AI OR climate OR politics -is:retweet", max_results=10, tweet_fields=["text"])
    
    if tweets.data:
        for tweet in tweets.data:
            post = SocialMediaPost(content=tweet.text, sentiment="neutral")
            db.add(post)
            broadcast_message(f"🐦 New Tweet: {tweet.text}")
    
    db.commit()
\@celery_app.task
def fetch_twitter_data_task():
    fetch_twitter_data_sync()

async def fetch_twitter_data_async():
    """Fetch Twitter data asynchronously using asyncio."""
    db = SessionLocal()
    query = "AI OR climate OR politics -is:retweet"
    
    while True:
        try:
            tweets = client.search_recent_tweets(query=query, max_results=10, tweet_fields=["text"])
            if tweets.data:
                for tweet in tweets.data:
                    post = SocialMediaPost(content=tweet.text, sentiment="neutral")
                    db.add(post)
                    await broadcast_message(f"🐦 New Tweet: {tweet.text}")
            
            db.commit()
        except Exception as e:
            print(f"Error fetching tweets: {e}")

        await asyncio.sleep(10)  # Fetch new tweets every 10 seconds
\@celery_app.task
def fetch_twitter_data_task():
    asyncio.run(fetch_twitter_data_async())