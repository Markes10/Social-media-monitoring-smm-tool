from fastapi import APIRouter
import sqlite3
from collections import Counter

router = APIRouter()

@router.get("/get_sentiment_trends")
def get_sentiment_trends():
    """Fetch sentiment trend data"""
    conn = sqlite3.connect("smm_tool.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sentiment, COUNT(*) as count 
        FROM SentimentAnalysis 
        GROUP BY sentiment
    """)
    
    trends = cursor.fetchall()
    conn.close()

    return {"trends": [{"sentiment": row[0], "count": row[1]} for row in trends]}

@router.get("/get_trending_data")
def get_trending_data():
    """Fetch top trending hashtags and keywords"""
    conn = sqlite3.connect("smm_tool.db")
    cursor = conn.cursor()

    cursor.execute("SELECT hashtags, keywords FROM TrendingData")
    data = cursor.fetchall()
    conn.close()

    hashtag_list = []
    keyword_list = []

    for row in data:
        if row[0]: hashtag_list.extend(row[0].split(", "))
        if row[1]: keyword_list.extend(row[1].split(", "))

    trending_hashtags = Counter(hashtag_list).most_common(5)
    trending_keywords = Counter(keyword_list).most_common(5)

    return {
        "hashtags": [{"hashtag": tag, "count": count} for tag, count in trending_hashtags],
        "keywords": [{"keyword": word, "count": count} for word, count in trending_keywords],
    }
