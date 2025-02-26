from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Competitor
from auth import get_current_user
from competitor_analysis import analyze_competitor_performance, get_competitor_analysis, benchmark_performance, fetch_competitor_metrics
from competitor_scraper import fetch_competitor_posts, analyze_trending_content
from instagram_competitor import fetch_instagram_competitor
from twitter_competitor import fetch_twitter_competitor

router = APIRouter()

@router.get("/competitor-analysis")
def competitor_analysis():
    """Fetch AI-driven competitor analysis insights."""
    return {"competitor_insights": analyze_competitor_performance()}

@router.get("/competitor/social-insights")
def fetch_social_insights():
    """Fetch AI-powered competitor social media insights."""
    return {"competitor_insights": get_competitor_analysis()}

@router.get("/competitor/posts")
def get_competitor_posts(url: str):
    """Fetch latest posts from a competitor."""
    return fetch_competitor_posts(url)

@router.post("/competitor/trending")
def get_trending_content(posts_data: list):
    """Analyze trending competitor posts."""
    return analyze_trending_content(posts_data)

@router.post("/competitors/analyze")
def analyze_competitors(competitors: list):
    """Fetch engagement metrics for competitors."""
    return fetch_competitor_metrics(competitors)

@router.get("/competitor/performance")
def get_competitor_performance(username: str, platform: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetch and analyze competitor performance on a specific platform."""
    competitor_data = None
    if platform.lower() == "instagram":
        competitor_data = fetch_instagram_competitor(username)
    elif platform.lower() == "twitter":
        competitor_data = fetch_twitter_competitor(username)
    return {"competitor_analysis": competitor_data} if competitor_data else {"error": "Competitor data not found"}

@router.get("/competitor/benchmark")
def benchmark_competitor():
    """Fetch AI-driven competitor benchmarking insights."""
    insights = benchmark_performance()
    return {"competitor_data": insights}
