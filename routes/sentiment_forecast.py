from fastapi import APIRouter
from forecast_sentiment import forecast_sentiment

router = APIRouter()

@router.get("/forecast_sentiment")
def get_sentiment_forecast(topic: str):
    """Predict future sentiment trends for a topic"""
    return {"forecast": forecast_sentiment(topic)}
