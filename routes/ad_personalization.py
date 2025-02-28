from fastapi import APIRouter
from sentiment_analysis import process_sentiment_data
from ai_ad_personalization import personalize_ads

router = APIRouter()

@router.get("/personalize_ads")
def get_personalized_ads():
    """Fetch AI-generated personalized ads based on sentiment"""
    sentiment_data = process_sentiment_data()
    recommendations = personalize_ads(sentiment_data)
    return {"personalized_ads": recommendations}
