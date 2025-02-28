from fastapi import APIRouter
from fetch_trending import fetch_trending_topics
from predict_virality import predict_virality
from trend_prediction import train_trend_model

router = APIRouter()

@router.get("/trending_topics")
def get_trending_topics():
    """Retrieve trending hashtags and topics."""
    return {"trending_topics": fetch_trending_topics()}

@router.get("/predict_virality")
def get_virality_prediction(content: str, likes: int, shares: int):
    """Predict virality of a post."""
    engagement_metrics = {"likes": likes, "shares": shares}
    return {"prediction": predict_virality(content, engagement_metrics)}

@router.post("/predict-trends")
def predict_trends(data: list):
    """Predict future social media trends based on past engagement data."""
    predictions = train_trend_model(data)
    return {"predictions": predictions}
