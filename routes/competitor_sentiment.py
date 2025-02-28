from fastapi import APIRouter
from competitor_scraper import scrape_competitor

router = APIRouter()

@router.get("/competitor_sentiment")
def get_competitor_sentiment(competitor: str, limit: int = 50):
    """Analyze competitor PR sentiment"""
    return {"data": scrape_competitor(competitor, limit)}
