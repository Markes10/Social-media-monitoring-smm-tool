from fastapi import APIRouter
from social_listening import fetch_social_conversations, detect_trends

router = APIRouter()

@router.get("/social/listening")
def get_social_conversations(platform: str, keyword: str):
    """Fetch latest social media conversations based on keyword search."""
    return fetch_social_conversations(platform, keyword)

@router.post("/social/trends")
def analyze_social_trends(posts: list):
    """Analyze trending social media topics."""
    return detect_trends(posts)
