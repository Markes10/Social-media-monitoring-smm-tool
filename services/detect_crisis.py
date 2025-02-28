import time
from sentiment_analysis import analyze_sentiment
from fetch_trending import fetch_trending_topics

def detect_crisis():
    """Detects negative PR or crisis trends based on sentiment analysis"""
    
    trending_topics = fetch_trending_topics()
    crisis_alerts = []
    
    for topic in trending_topics:
        sentiment = analyze_sentiment(topic["name"])
        
        if sentiment.lower() == "negative":
            crisis_alerts.append({"topic": topic["name"], "tweets": topic["tweet_volume"], "alert": "⚠️ Potential Crisis!"})

    return crisis_alerts

# Example usage:
# print(detect_crisis())
