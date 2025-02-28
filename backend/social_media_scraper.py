import asyncio
import requests
from database import SessionLocal
from models import SocialMediaPost
from routes.realtime import broadcast_message, check_negative_sentiment

async def fetch_social_media():
    """Fetches latest social media posts and processes sentiment analysis."""
    db = SessionLocal()
    while True:
        response = requests.get("https://api.example.com/latest-posts")  # Replace with real API
        posts = response.json()

        for post in posts:
            new_post = SocialMediaPost(content=post["text"], sentiment=post["sentiment"])
            db.add(new_post)
            message = f"New Post: {post['text']} - Sentiment: {post['sentiment']}"
            if post["sentiment"] == "negative":
                message = f"🚨 Negative Post Detected: {post['text']}"
            await broadcast_message(message)

        db.commit()
        check_negative_sentiment(db)  # Check if alert needs to be triggered
        await asyncio.sleep(10)  # Fetch new posts every 10 seconds
