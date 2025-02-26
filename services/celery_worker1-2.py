import os
import datetime
import tweepy
import requests
from celery import Celery
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from models import ScheduledPost

# Load environment variables
load_dotenv()

# Celery Configuration
BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery = Celery("tasks", broker=BROKER_URL)

# Twitter API Authentication
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")


def post_to_twitter(content):
    """Posts content to Twitter using Tweepy."""
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    api = tweepy.API(auth)
    
    try:
        api.update_status(content)
        return True
    except Exception as e:
        print(f"❌ Twitter post failed: {e}")
        return False


def post_to_facebook(content):
    """Posts content to Facebook using Graph API."""
    api_url = f"https://graph.facebook.com/{os.getenv('FACEBOOK_PAGE_ID')}/feed"
    params = {
        "message": content,
        "access_token": os.getenv("FACEBOOK_ACCESS_TOKEN"),
    }
    response = requests.post(api_url, params=params)
    return response.json()


def post_to_social_media(platform, content):
    """Posts content to the specified social media platform."""
    if platform == "twitter":
        return post_to_twitter(content)
    elif platform == "facebook":
        return post_to_facebook(content)
    return False  


@celery.task
def post_scheduled_posts():
    """Checks for scheduled posts and publishes them automatically."""
    db: Session = SessionLocal()
    now = datetime.datetime.utcnow()
    posts = db.query(ScheduledPost).filter(ScheduledPost.scheduled_time <= now, ScheduledPost.posted == False).all()

    for post in posts:
        success = post_to_social_media(post.platform, post.content)
        if success:
            post.posted = True
            post.status = "posted"
        else:
            post.status = "failed"
    
    db.commit()
    db.close()


@celery.task
def schedule_post(content, platform, scheduled_time):
    """Schedules a post for a specific platform at a given time."""
    post = ScheduledPost(content=content, platform=platform, scheduled_time=scheduled_time, posted=False, status="scheduled")
    db: Session = SessionLocal()
    db.add(post)
    db.commit()
    db.close()
    return {"message": "Post scheduled successfully!"}

# Example usage:
# schedule_post("Hello World!", "twitter", datetime.datetime.utcnow())
# post_scheduled_posts()