from fastapi import APIRouter
from content_generator import generate_post
from content_optimizer import suggest_best_time, generate_caption
from content_prediction import predict_post_performance

router = APIRouter()

@router.get("/generate-content")
def fetch_generated_content(topic: str, tone: str = "casual"):
    """Fetch AI-powered social media content."""
    return {"generated_post": generate_post(topic, tone)}

@router.post("/content/best-time")
def best_posting_time(posts_data: list):
    """Suggest the best time to post based on past engagement."""
    return {"best_time": suggest_best_time(posts_data)}

@router.post("/content/generate-caption")
def ai_generated_caption(prompt: str):
    """Generate AI-powered captions."""
    return {"caption": generate_caption(prompt)}

@router.get("/content-prediction")
def get_content_prediction(word_count: int, image_count: int, hashtag_count: int, post_hour: int):
    """Predicts the engagement of a social media post."""
    engagement = predict_post_performance(word_count, image_count, hashtag_count, post_hour)
    return {"predicted_engagement": engagement}
