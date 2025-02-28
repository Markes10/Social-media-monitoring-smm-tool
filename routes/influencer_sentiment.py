from fastapi import APIRouter
from influencer_analysis import analyze_influencer

router = APIRouter()

@router.get("/influencer_sentiment")
def get_influencer_sentiment(influencer: str, limit: int = 50):
    """Analyze influencer impact on brand sentiment"""
    return {"data": analyze_influencer(influencer, limit)}
