from fastapi import APIRouter
from hashtag_analysis import extract_hashtags, fetch_trending_hashtags, analyze_hashtag_engagement, analyze_hashtags

router = APIRouter()

@router.post("/hashtag-analysis")
def get_hashtags(data: dict):
    """Fetch AI-driven hashtag suggestions."""
    text = data.get("text", "")
    hashtags_result = extract_hashtags(text)
    return {"hashtag_data": hashtags_result}

@router.get("/hashtags/trending")
def get_trending_hashtags(location_woeid: int = 1):
    """Fetch top trending hashtags."""
    return fetch_trending_hashtags(location_woeid)

@router.get("/hashtags/analyze")
def get_hashtag_analysis(hashtag: str):
    """Analyze engagement for a hashtag."""
    return analyze_hashtag_engagement(hashtag)

@router.get("/hashtag-insights")
def get_hashtag_insights():
    """Fetch AI-driven hashtag and trend analysis insights."""
    return {"hashtag_insights": analyze_hashtags()}
