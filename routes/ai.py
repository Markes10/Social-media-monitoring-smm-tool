from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Agency
from ai_content import generate_post_suggestions, recommend_hashtags
from auth import get_current_user

router = APIRouter()

@router.get("/generate-posts")
def get_post_suggestions(user=Depends(get_current_user), db: Session = Depends(get_db)):
    agency = db.query(Agency).filter(Agency.id == user.agency_id).first()
    
    if not agency:
        return {"message": "Agency not found"}

    post_ideas = generate_post_suggestions(agency.name, "healthcare" if "clinic" in agency.name.lower() else "business")
    
    return {"post_suggestions": post_ideas}

@router.post("/generate-hashtags")
def get_hashtags(content: str):
    hashtags = recommend_hashtags(content)
    return {"hashtags": hashtags}
