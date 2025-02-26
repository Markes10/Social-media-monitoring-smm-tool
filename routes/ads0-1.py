from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import AdPerformance
from ad_performance import fetch_facebook_ads, fetch_google_ads, fetch_twitter_ads
from ml_ad_performance import predict_best_ad
from auth import get_current_user

router = APIRouter()

@router.get("/ad-performance")
def get_ad_performance(user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetches AI-powered ad performance insights."""
    facebook_ads = fetch_facebook_ads()
    insights = []
    for ad in facebook_ads:
        predicted_score = predict_best_ad(ad["impressions"], ad["clicks"], ad["conversions"])
        insights.append({
            "ad_name": ad["ad_name"],
            "impressions": ad["impressions"],
            "clicks": ad["clicks"],
            "conversions": ad["conversions"],
            "cost_per_click": ad["cost_per_click"],
            "predicted_engagement_score": predicted_score
        })
    return {"ad_performance_insights": insights}

@router.get("/ads/facebook")
def fetch_fb_ads():
    """Fetch Facebook Ad performance metrics."""
    return fetch_facebook_ads()

@router.get("/ads/google")
def fetch_google_ads_data():
    """Fetch Google Ad performance metrics."""
    return fetch_google_ads()

@router.get("/ads/twitter")
def fetch_twitter_ads_data():
    """Fetch Twitter Ad performance metrics."""
    return fetch_twitter_ads()