from fastapi import APIRouter
from influencer_analysis import get_influencers

router = APIRouter()

@router.get("/influencers")
def fetch_influencers(brand: str, count: int = 100):
    """Get top influencers for a brand"""
    return get_influencers(brand, count)
