from fastapi import APIRouter
from ad_optimizer import optimize_ad_budget
from ad_performance import optimize_ad_performance

router = APIRouter()

@router.get("/ad-optimization/budget")
def ad_optimization(ad_spend: float, ctr: float, conversion_rate: float):
    """Optimize ad budget for better ROI."""
    optimized_budget = optimize_ad_budget(ad_spend, ctr, conversion_rate)
    return {"optimized_budget": optimized_budget}

@router.get("/ad-optimization/performance")
def get_ad_optimization():
    """Fetch AI-driven ad performance insights."""
    insights = optimize_ad_performance()
    return {"ad_data": insights}