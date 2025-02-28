from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from competitor_analysis import compare_with_competitor

router = APIRouter()

@router.get("/competitor-insights")
def get_competitor_insights(user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetches AI-based competitor insights."""
    
    insights = compare_with_competitor(user.agency_id)
    return {"competitor_insights": insights}
