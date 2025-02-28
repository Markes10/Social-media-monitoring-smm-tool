from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime
from database import get_db
from models import SocialMediaPost

router = APIRouter()

# Extract trending hashtags
@router.get("/hashtags")
def get_trending_hashtags(platform: str = None, start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    query = db.query(SocialMediaPost.content)

    if platform:
        query = query.filter(SocialMediaPost.platform == platform)
    
    if start_date and end_date:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.filter(and_(SocialMediaPost.created_at >= start_dt, SocialMediaPost.created_at <= end_dt))

    hashtags = {}
    for post in query.all():
        words = post.content.split()
        for word in words:
            if word.startswith("#"):
                hashtags[word] = hashtags.get(word, 0) + 1

    sorted_hashtags = sorted(hashtags.items(), key=lambda x: x[1], reverse=True)
    return [{"hashtag": h[0], "count": h[1]} for h in sorted_hashtags[:10]]  # Return top 10 hashtags

# Keyword Sentiment Analysis
@router.get("/keyword-analysis")
def keyword_sentiment_analysis(keyword: str, db: Session = Depends(get_db)):
    keyword = f"%{keyword}%"
    query = db.query(SocialMediaPost.sentiment, func.count(SocialMediaPost.id)).filter(SocialMediaPost.content.like(keyword)).group_by(SocialMediaPost.sentiment)

    sentiment_counts = {row[0]: row[1] for row in query.all()}
    return {
        "keyword": keyword,
        "Positive": sentiment_counts.get("Positive", 0),
        "Negative": sentiment_counts.get("Negative", 0),
        "Neutral": sentiment_counts.get("Neutral", 0),
    }
