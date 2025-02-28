from fastapi import APIRouter
from influencer_analysis import get_top_influencers
from ai_influencer_match import suggest_influencer_partnerships
from ai_influencer_recommendations import recommend_collaborations

router = APIRouter()

@router.get("/influencer_strategy")
def influencer_strategy(brand: str, category: str):
    """Fetch top influencers & AI-powered recommendations"""
    influencers = get_top_influencers(category)
    partnership_strategy = suggest_influencer_partnerships(brand, influencers)
    recommendations = recommend_collaborations(influencers)
    
    return {
        "top_influencers": influencers,
        "partnership_strategy": partnership_strategy,
        "recommendations": recommendations
    }
