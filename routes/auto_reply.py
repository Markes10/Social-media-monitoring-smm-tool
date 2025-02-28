from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import SocialMediaPost
from auto_response import generate_response, generate_auto_reply
from sentiment_analysis import analyze_sentiment

router = APIRouter()

@router.get("/generate_auto_reply")
def fetch_auto_reply(brand: str, comment: str, sentiment: str):
    """Generate an AI-powered auto-reply for social media comments"""
    return {"reply": generate_auto_reply(brand, comment, sentiment)}

@router.get("/auto_reply")
def get_auto_reply(brand: str, message: str):
    """Generate an AI-powered reply for a given customer message."""
    reply = generate_auto_reply(brand, message)
    return {"brand": brand, "customer_message": message, "ai_reply": reply}

@router.post("/auto-reply/{post_id}")
def auto_reply_by_post(post_id: int, db: Session = Depends(get_db)):
    """Generate an automated reply for a post if it has negative sentiment."""
    post = db.query(SocialMediaPost).filter(SocialMediaPost.id == post_id).first()
    
    if not post:
        return {"message": "Post not found"}
    
    if post.sentiment != "negative":
        return {"message": "Auto-reply only for negative posts"}
    
    reply = generate_response(post.content)
    return {"post_id": post_id, "auto_reply": reply}

@router.post("/auto-reply")
def auto_reply_by_text(text: str):
    """Generate an auto-reply based on sentiment analysis."""
    sentiment = analyze_sentiment(text)["vader_sentiment"]
    reply = generate_auto_reply(text, sentiment)
    return {"auto_reply": reply}
