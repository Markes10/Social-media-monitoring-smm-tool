from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from database import get_db
from models import SocialMediaPost, Analytics, PostAnalytics
from auth import get_current_user
from ml_trends import predict_engagement
from analytics import fetch_engagement_metrics, get_sentiment_trends, generate_insights, predict_sentiment_trends, get_topics
import numpy as np

router = APIRouter()

@router.get("/social-analytics")
def social_analytics(platform: str, brand: str):
    """Return engagement & sentiment trends for a brand."""
    engagement = fetch_engagement_metrics(platform, brand)
    sentiment = get_sentiment_trends(platform, brand)
    return {"engagement": engagement, "sentiment_trends": sentiment}

@router.get("/analytics")
def get_analytics(user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetch AI-driven social media performance insights."""
    agency_id = user.agency_id
    total_posts = db.query(SocialMediaPost).filter(SocialMediaPost.agency_id == agency_id).count()
    avg_sentiment = db.query(func.avg(SocialMediaPost.sentiment_score)).filter(SocialMediaPost.agency_id == agency_id).scalar() or 0.0
    engagement_rate = total_posts * avg_sentiment  # Simple calculation
    analytics = Analytics(agency_id=agency_id, total_posts=total_posts, avg_sentiment_score=avg_sentiment, engagement_rate=engagement_rate)
    db.add(analytics)
    db.commit()
    insights = generate_insights()
    return {"total_posts": total_posts, "avg_sentiment_score": avg_sentiment, "engagement_rate": engagement_rate, "analytics_data": insights}

@router.get("/sentiment-trends")
def sentiment_trends(days: int = 7, db: Session = Depends(get_db)):
    return get_sentiment_trends(days)

@router.get("/trending-topics")
def trending_topics():
    return get_topics()

@router.get("/predict-sentiment")
def predict_sentiment(days: int = 7):
    return predict_sentiment_trends(days)

@router.get("/predict-engagement")
def get_predicted_engagement(user=Depends(get_current_user)):
    return predict_engagement(user.agency_id)

@router.get("/post-performance/{post_id}")
def get_post_performance(post_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetches analytics for a specific post."""
    analytics = db.query(PostAnalytics).filter(PostAnalytics.post_id == post_id).first()
    if not analytics:
        return {"message": "No analytics found for this post"}
    return {"likes": analytics.likes, "shares": analytics.shares, "comments": analytics.comments, "impressions": analytics.impressions, "engagement_score": analytics.engagement_score}

@router.get("/best-performing-posts")
def best_performing_posts(user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Finds the best-performing posts based on engagement score."""
    posts = db.query(PostAnalytics).order_by(PostAnalytics.engagement_score.desc()).limit(5).all()
    return [{"post_id": p.post_id, "engagement_score": p.engagement_score, "platform": p.platform} for p in posts]
