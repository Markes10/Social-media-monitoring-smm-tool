from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import SocialMention
from auth import get_current_user

router = APIRouter()

@router.get("/mentions")
def get_mentions(user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetches brand mentions for the user’s agency."""
    
    mentions = db.query(SocialMention).filter(SocialMention.agency_id == user.agency_id).order_by(SocialMention.timestamp.desc()).all()

    return [
        {
            "platform": mention.platform,
            "mention_text": mention.mention_text,
            "user_handle": mention.user_handle,
            "sentiment": mention.sentiment,
            "timestamp": mention.timestamp
        }
        for mention in mentions
    ]
