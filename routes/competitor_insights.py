from fastapi import APIRouter
from competitor_analysis import scrape_competitor_tweets, analyze_competitor_trends

router = APIRouter()

@router.get("/competitor_insights")
def get_competitor_insights(competitor: str):
    """Fetch & analyze competitor social media activity."""
    tweets_df = scrape_competitor_tweets(competitor, 20)
    insights = analyze_competitor_trends(tweets_df)
    return {"competitor": competitor, "ai_insights": insights}
