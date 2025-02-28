from fastapi import APIRouter
from sentiment_analysis import analyze_sentiment
from engagement_predictor import predict_engagement

router = APIRouter()

@router.get("/analyze_sentiment")
def get_sentiment(text: str):
    """Get sentiment analysis of a post"""
    return analyze_sentiment(text)

@router.get("/predict_engagement")
def get_engagement_prediction(text: str):
    """Predict engagement metrics for a post"""
    return predict_engagement(text)
