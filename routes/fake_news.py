from fastapi import APIRouter
from fake_news_detector import fetch_social_posts, detect_fake_news

router = APIRouter()

@router.get("/fake-news/posts")
def get_social_posts(platform: str, keyword: str):
    """Fetch latest social media posts based on keyword search."""
    return fetch_social_posts(platform, keyword)

@router.post("/fake-news/analyze")
def analyze_fake_news(posts: list):
    """Analyze social media posts for misinformation."""
    return detect_fake_news(posts)
