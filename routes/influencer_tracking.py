from fastapi import APIRouter
from fetch_influencers import fetch_top_influencers

router = APIRouter()

@router.get("/top_influencers")
def get_top_influencers(brand_handle: str, limit: int = 10):
    """Retrieve top influencers interacting with the brand"""
    return {"influencers": fetch_top_influencers(brand_handle, limit)}
