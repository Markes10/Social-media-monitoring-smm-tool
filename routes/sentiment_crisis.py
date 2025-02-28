from fastapi import APIRouter
from sentiment_analysis import analyze_sentiment
from detect_crisis import detect_crisis

router = APIRouter()

@router.get("/analyze_sentiment")
def get_sentiment(text: str):
    """Analyze sentiment of a given text"""
    return {"sentiment": analyze_sentiment(text)}

@router.get("/crisis_alerts")
def get_crisis_alerts():
    """Detect negative PR and crisis situations"""
    return {"crisis_alerts": detect_crisis()}
