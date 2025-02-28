from fastapi import APIRouter
from ai_content import generate_social_media_post
from trending_topics import get_trending_topics
from content_recommendation import generate_content_recommendation
import joblib

router = APIRouter()

# Load trained engagement prediction model
engagement_model = joblib.load("engagement_predictor.pkl")

@router.get("/ai-content")
def get_ai_content(topic: str, audience: str, platform: str):
    """Generate AI-driven social media post."""
    post = generate_social_media_post(topic, audience, platform)
    return {"post": post}

@router.get("/trending-topics")
def get_trending():
    """Fetch trending Twitter topics."""
    return {"trending": get_trending_topics()}

@router.post("/predict-engagement")
def predict_engagement(text: str):
    """Predict engagement for a post."""
    text_length = len(text)
    prediction = engagement_model.predict([[text_length]])
    return {"predicted_likes": prediction[0][0], "predicted_shares": prediction[0][1], "predicted_comments": prediction[0][2]}

@router.get("/content-strategy")
def content_strategy(brand: str, trend: str, sentiment: str):
    """Generate AI-powered content recommendations."""
    recommendations = generate_content_recommendation(brand, trend, sentiment)
    return {"recommendations": recommendations}
