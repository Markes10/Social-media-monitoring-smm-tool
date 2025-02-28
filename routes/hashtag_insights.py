from fastapi import APIRouter
from hashtag_analysis import analyze_hashtag_sentiment

router = APIRouter()

@router.get("/hashtag_insights/{hashtag}")
def get_hashtag_insights(hashtag: str):
    """Fetch AI-powered sentiment insights for hashtags"""
    insights = analyze_hashtag_sentiment(hashtag)
    return insights
