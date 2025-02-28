from fastapi import APIRouter
from social_listening import get_brand_mentions
from ai_trend_detector import detect_trends

router = APIRouter()

@router.get("/social_listening")
def social_listening(brand: str):
    """Fetch brand mentions & AI-powered trend detection"""
    data = get_brand_mentions(brand)
    trends = detect_trends(data)
    return {"brand_mentions": data, "trend_analysis": trends}
