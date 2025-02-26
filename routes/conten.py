from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ContentRecommendation
from auth import get_current_user
from ai_caption_generator import generate_post_caption
from ml_posting_time import recommend_best_posting_time

router = APIRouter()

@router.get("/content-recommendations")
def get_content_recommendations(user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetches AI-powered content recommendations."""
    
    best_time = recommend_best_posting_time()
    caption = generate_post_caption("latest trends in marketing")

    return {
        "recommended_caption": caption,
        "best_posting_time": best_time,
        "suggested_hashtags": "#marketing #trending #growth"
    }
