import tweepy
import asyncio
from database import SessionLocal
from models import SocialMediaPost
from routes.realtime import broadcast_message

# Twitter API Credentials
BEARER_TOKEN = "YOUR_TWITTER_BEARER_TOKEN"

# Set up Tweepy Client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Function to Stream Tweets
async def fetch_twitter_data():
    db = SessionLocal()
    query = "AI OR climate OR politics -is:retweet"  # Modify query for topics of interest

    while True:
        try:
            tweets = client.search_recent_tweets(query=query, max_results=10, tweet_fields=["text"])
            for tweet in tweets.data:
                post = SocialMediaPost(content=tweet.text, sentiment="neutral")  # Add sentiment analysis
                db.add(post)
                await broadcast_message(f"🐦 New Tweet: {tweet.text}")
            
            db.commit()
        except Exception as e:
            print(f"Error fetching tweets: {e}")

        await asyncio.sleep(10)  # Fetch new tweets every 10 seconds
