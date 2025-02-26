from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from models import SocialMediaPost
from moderation import moderate_content
from ai_sentiment import analyze_sentiment

router = APIRouter()

@router.post("/add-post")
def add_post(post: SocialMediaPost, db: Session = Depends(get_db)):
    """Add a new post with moderation check."""
    moderation_result = moderate_content(post.content)
    
    if moderation_result["flagged"]:
        return {"message": "Post flagged for moderation", "reason": moderation_result["reason"]}
    
    db.add(post)
    db.commit()
    return {"message": "Post added successfully"}

@router.get("/posts")
def get_posts(user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetch posts belonging to the user's agency."""
    return db.query(SocialMediaPost).filter(SocialMediaPost.agency_id == user.agency_id).all()

@router.post("/create-post")
def create_post(content: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new post with sentiment analysis."""
    sentiment_score = analyze_sentiment(content)
    post = SocialMediaPost(content=content, agency_id=user.agency_id, sentiment_score=sentiment_score)
    db.add(post)
    db.commit()
    
    return {"message": "Post created successfully", "sentiment_score": sentiment_score}
