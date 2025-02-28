from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from database import get_db
from models import SocialMediaPost

router = APIRouter()

@router.get("/posts")
def list_posts(platform: str = None, start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    query = db.query(SocialMediaPost)

    if platform:
        query = query.filter(SocialMediaPost.platform == platform)
    
    if start_date and end_date:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.filter(and_(SocialMediaPost.created_at >= start_dt, SocialMediaPost.created_at <= end_dt))

    return query.all()
