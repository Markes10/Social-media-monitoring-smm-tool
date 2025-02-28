from fastapi import APIRouter
from hashtag_predictor import train_hashtag_model, predict_hashtag_performance
from content_recommender import generate_content_ideas

router = APIRouter()

model = train_hashtag_model()

@router.get("/predict_hashtag/{hashtag}")
def get_hashtag_prediction(hashtag: str):
    """Predict hashtag engagement"""
    hashtag_data = {"posts": 100, "likes": 500, "shares": 300, "comments": 200}  # Placeholder
    prediction = predict_hashtag_performance(model, hashtag_data)
    return prediction

@router.get("/recommend_content")
def get_content_recommendations():
    """Fetch AI-powered content ideas"""
    return {"content_ideas": generate_content_ideas()}
