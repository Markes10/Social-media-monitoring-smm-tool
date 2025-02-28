from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests
import os
from database import get_db
from models import SocialMediaComment
from twitter_scraper import fetch_twitter_comments
from facebook_scraper import fetch_facebook_comments
from sentiment_analysis import analyze_sentiment, fetch_social_posts, brand_sentiment_analysis
from monitor_mentions import detect_crisis
from auth import get_current_user

router = APIRouter()

@router.post("/analyze-sentiment")
def analyze_comment(comment: str):
    """Analyze sentiment of a comment."""
    return analyze_sentiment(comment)

@router.get("/detect-crisis")
def detect_crisis_event(platform: str, post_id: str):
    """Detect crisis based on negative sentiment trends."""
    api_url = f"https://api.twitter.com/2/tweets/{post_id}/comments" if platform == "twitter" else \
              f"https://graph.facebook.com/{post_id}/comments?access_token={os.getenv('FACEBOOK_ACCESS_TOKEN')}"
    response = requests.get(api_url).json()
    comments = response.get("data", [])
    negative_count = sum(1 for comment in comments if analyze_sentiment(comment["text"])['label'] == "NEGATIVE")
    crisis_detected = negative_count / len(comments) > 0.5 if comments else False
    return {"crisis_detected": crisis_detected, "negative_comments": negative_count}

@router.get("/sentiment/posts")
def get_social_posts(platform: str, keyword: str):
    """Fetch latest social media posts based on keyword search."""
    return fetch_social_posts(platform, keyword)

@router.post("/sentiment/analyze")
def analyze_social_sentiment(posts: list):
    """Analyze sentiment of social media posts."""
    return analyze_sentiment(posts)

@router.get("/sentiment/brand")
def get_brand_sentiment(brand: str, count: int = 100):
    """Analyze sentiment for a brand."""
    return brand_sentiment_analysis(brand, count)

@router.get("/social-sentiment")
def get_social_sentiment(keyword: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetches and analyzes sentiment of social media comments."""
    twitter_comments = fetch_twitter_comments(keyword)
    facebook_comments = fetch_facebook_comments()
    all_comments = twitter_comments + facebook_comments
    sentiment_results = [{
        "platform": comment["platform"],
        "username": comment["username"],
        "comment_text": comment["comment_text"],
        "sentiment": analyze_sentiment(comment["comment_text"])
    } for comment in all_comments]
    return {"sentiment_analysis": sentiment_results}

@router.get("/crisis-detection")
def check_crisis(brand: str, platform: str):
    """Check for PR crisis alerts."""
    return {"crisis_alert": detect_crisis(brand, platform)}

@router.post("/sentiment-analysis")
def get_sentiment(data: dict):
    """Fetch AI-driven sentiment insights."""
    return {"sentiment_data": analyze_sentiment(data.get("text", ""))}
