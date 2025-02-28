from fastapi import APIRouter
from predict_sentiment import predict_sentiment

router = APIRouter()

@router.get("/predict_sentiment")
def fetch_sentiment_prediction(brand: str):
    """Predict future sentiment for a brand"""
    return predict_sentiment(brand)
