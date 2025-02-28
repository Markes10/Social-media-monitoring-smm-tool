from fastapi import APIRouter
from ad_performance import get_ad_performance
from ai_ad_optimizer import optimize_ad_strategy

router = APIRouter()

@router.get("/ad_optimization")
def ad_optimization(platform: str):
    """Fetch ad performance & AI-powered recommendations"""
    data = get_ad_performance(platform)
    insights = optimize_ad_strategy(data)
    return {"ad_performance": data, "recommendations": insights}
