import random
import pandas as pd
from textblob import TextBlob
from transformers import pipeline

# AI sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# Simulated audience engagement data (normally fetched via API)
engagement_data = [
    {"comment": "This post is amazing! Love the insights!", "likes": 120, "shares": 15},
    {"comment": "Not really helpful, I expected more details.", "likes": 45, "shares": 5},
    {"comment": "Wow! Great content, very informative!", "likes": 200, "shares": 30},
    {"comment": "I completely disagree with this post.", "likes": 30, "shares": 3},
    {"comment": "Very useful tips, will definitely try them out!", "likes": 150, "shares": 20}
]

def analyze_sentiment(comment):
    """Analyze sentiment of a given comment."""
    result = sentiment_analyzer(comment)
    return result[0]["label"]

def get_engagement_insights():
    """Analyze audience engagement and sentiment trends."""
    insights = []
    total_likes = 0
    total_shares = 0

    for entry in engagement_data:
        sentiment = analyze_sentiment(entry["comment"])
        total_likes += entry["likes"]
        total_shares += entry["shares"]
        insights.append({
            "comment": entry["comment"],
            "sentiment": sentiment,
            "likes": entry["likes"],
            "shares": entry["shares"]
        })

    avg_likes = total_likes / len(engagement_data)
    avg_shares = total_shares / len(engagement_data)

    return {
        "engagement_insights": insights,
        "average_likes": avg_likes,
        "average_shares": avg_shares
    }

# Example usage:
# print(get_engagement_insights())
