from fastapi import APIRouter
from services.sentiment_analysis import analyze_sentiment

router = APIRouter()

@router.get("/analyze")
def analyze():
    analyze_sentiment()
    return {"message": "Sentiment analysis completed"}
