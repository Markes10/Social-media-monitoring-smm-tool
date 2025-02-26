import pandas as pd
import numpy as np
from transformers import pipeline
from datetime import datetime, timedelta

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# Sample social media posts (normally fetched from Twitter, Facebook, etc.)
def detect_crisis(social_media_posts=None):
    """Detect a potential PR crisis by analyzing sentiment trends."""
    
    if social_media_posts is None:
        social_media_posts = [
            {"text": "I love this product! Amazing quality. #HappyCustomer", "timestamp": datetime.now() - timedelta(hours=2)},
            {"text": "Worst experience ever. Never buying again. #Disappointed", "timestamp": datetime.now() - timedelta(hours=1)},
            {"text": "This company is a scam! Avoid at all costs!", "timestamp": datetime.now()},
            {"text": "Great customer service! They really care about customers.", "timestamp": datetime.now() - timedelta(minutes=30)},
        ]
    
    crisis_alerts = []
    sentiments = [sentiment_analyzer(post["text"])[0] for post in social_media_posts]
    
    negative_count = 0
    for idx, sentiment in enumerate(sentiments):
        if sentiment["label"] == "NEGATIVE":
            negative_count += 1
            if sentiment["score"] > 0.8:
                crisis_alerts.append({
                    "text": social_media_posts[idx]["text"],
                    "timestamp": social_media_posts[idx]["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                    "alert_level": "HIGH",
                    "recommendation": "Immediate response required! Address customer concerns publicly and offer a resolution."
                })
    
    crisis_risk = (negative_count / len(social_media_posts)) * 100 if social_media_posts else 0
    response_strategy = "Monitor" if crisis_risk < 30 else "Alert Team & Respond Immediately"
    
    return {
        "crisis_detected": len(crisis_alerts) > 0,
        "negative_percentage": crisis_risk,
        "response_strategy": response_strategy,
        "alerts": crisis_alerts if crisis_alerts else "No crisis detected.",
        "details": sentiments
    }

# Example usage:
# posts = ["I hate this product!", "Worst customer service!", "Amazing experience!", "Terrible app!"]
# print(detect_crisis(posts))
