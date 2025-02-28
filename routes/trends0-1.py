from fastapi import APIRouter
from trend_analysis import get_trending_hashtags
from competitor_analysis import fetch_competitor_data

router = APIRouter()

@router.get("/trends")
def fetch_trends():
    """Fetch global trending hashtags."""
    return {"trending_hashtags": get_trending_hashtags()}

@router.get("/competitor")
def fetch_competitor(competitor_handle: str):
    """Fetch competitor engagement metrics."""
    return fetch_competitor_data(competitor_handle)
