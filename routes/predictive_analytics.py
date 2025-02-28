from fastapi import APIRouter
from engagement_data import fetch_engagement_data
from ai_trend_prediction import predict_social_trends

router = APIRouter()

@router.get("/predict_trends")
def predict_trends():
    """Fetch AI-driven social media trend predictions"""
    engagement_data = fetch_engagement_data()
    predictions = predict_social_trends(engagement_data)
    return {"trend_predictions": predictions}
