from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Influencer
from auth import get_current_user
from instagram_scraper import fetch_instagram_influencer
from twitter_scraper import fetch_twitter_influencer
from influencer_analysis import get_top_influencers, fetch_top_influencers, recommend_influencer
from influencer_detector import fetch_influencers, analyze_influencer_reach
from influencer_analytics import analyze_influencers
from fake_follower_detection import detect_fake_followers

router = APIRouter()

@router.get("/influencer-analysis")
def fetch_influencer_analysis():
    """Fetch AI-powered influencer insights."""
    return {"top_influencers": get_top_influencers()}

@router.get("/influencer-analytics")
def get_influencer_analytics():
    """Fetch AI-driven influencer performance insights."""
    insights = analyze_influencers()
    return {"influencer_data": insights}

@router.get("/influencer-recommendation")
def get_influencer_recommendation():
    """Fetch AI-driven influencer recommendations."""
    return {"influencer_data": recommend_influencer()}

@router.get("/influencer/instagram")
def fetch_ig_influencer(username: str):
    """Fetch Instagram influencer stats."""
    return fetch_instagram_influencer(username)

@router.get("/influencer/twitter")
def fetch_twitter_influencer_data(handle: str):
    """Fetch Twitter influencer stats."""
    return fetch_twitter_influencer(handle)

@router.get("/influencers")
def get_influencers(platform: str, keyword: str):
    """Fetch top influencers based on keyword search."""
    return fetch_influencers(platform, keyword)

@router.post("/influencers/analyze")
def analyze_reach(influencer_data: list):
    """Analyze influencer reach and engagement."""
    return analyze_influencer_reach(influencer_data)

@router.get("/influencers/top")
def get_top_influencers(hashtag: str):
    """Fetch top influencers based on engagement with a hashtag."""
    return fetch_top_influencers(hashtag)

@router.get("/influencer/performance")
def get_influencer_performance(username: str, platform: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetch and analyze influencer performance on a specific platform."""
    influencer_data = None
    if platform.lower() == "instagram":
        influencer_data = fetch_instagram_influencer(username)
    elif platform.lower() == "twitter":
        influencer_data = fetch_twitter_influencer(username)
    if influencer_data:
        fake_followers_percentage = detect_fake_followers(
            influencer_data["followers"],
            influencer_data["avg_likes"],
            influencer_data["avg_comments"]
        )
        influencer_data["fake_followers_percentage"] = fake_followers_percentage
        influencer_data["credibility_score"] = round(100 - fake_followers_percentage, 2)
        return {"influencer_analysis": influencer_data}
    return {"error": "Influencer data not found"}
