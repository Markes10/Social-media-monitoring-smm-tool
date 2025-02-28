from fastapi import APIRouter, Depends
from database import SessionLocal
from auth import require_role
from models import SocialMediaPost

router = APIRouter()

@router.get("/flagged-posts")
def get_flagged_posts(db: SessionLocal = Depends(), user=Depends(require_role("moderator"))):
    return db.query(SocialMediaPost).filter(SocialMediaPost.flagged == True).all()

@router.post("/approve-post/{post_id}")
def approve_post(post_id: int, db: SessionLocal = Depends(), user=Depends(require_role("admin"))):
    post = db.query(SocialMediaPost).filter(SocialMediaPost.id == post_id).first()
    if not post:
        return {"message": "Post not found"}
    
    post.flagged = False
    db.commit()
    return {"message": "Post approved"}
