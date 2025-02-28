from fastapi import APIRouter
from trend_prediction import predict_trend, extract_trending_keywords

router = APIRouter()

@router.get("/predict-trend")
def fetch_trend_prediction(hashtag: str):
    """Fetch AI-powered trend prediction for a specific hashtag."""
    return {"trend_forecast": predict_trend(hashtag)}

@router.post("/extract-keywords")
def fetch_trending_keywords(text: str):
    """Extract trending keywords from text using NLP."""
    return {"trending_keywords": extract_trending_keywords(text)}
