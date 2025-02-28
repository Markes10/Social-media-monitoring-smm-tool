from fastapi import APIRouter
from ad_performance_data import fetch_ad_performance
from ai_ad_optimization import optimize_ad_campaigns

router = APIRouter()

@router.get("/optimize_ads")
def optimize_ads():
    """Fetch AI-driven ad optimization recommendations"""
    ad_data = fetch_ad_performance()
    recommendations = optimize_ad_campaigns(ad_data)
    return {"ad_optimization": recommendations}
