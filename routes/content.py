from fastapi import APIRouter
from content_analysis import get_top_content
from ai_content_optimizer import optimize_content

router = APIRouter()

@router.get("/content_strategy")
def content_strategy(platform: str):
    """Fetch top content & AI-powered recommendations"""
    data = get_top_content(platform)
    insights = optimize_content(data)
    return {"top_content": data, "recommendations": insights}
