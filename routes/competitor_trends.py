from fastapi import APIRouter
from competitor_analysis import analyze_trends

router = APIRouter()

@router.get("/competitor_trends")
def get_competitor_trends():
    """Fetch top competitor trends"""
    trends = analyze_trends()
    return {"competitor_trends": trends}

