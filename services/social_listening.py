import requests
import pandas as pd
from collections import Counter
from transformers import pipeline

# Load AI model for trend detection
trend_analyzer = pipeline("text-classification", model="facebook/bart-large-mnli")

def fetch_social_conversations(platform, keyword):
    """Fetch recent social media posts based on a keyword."""
    if platform.lower() == "twitter":
        url = f"https://api.twitter.com/2/tweets/search/recent?query={keyword}"
        headers = {"Authorization": "Bearer YOUR_TWITTER_API_KEY"}
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": "Failed to fetch data"}

        tweets = response.json().get("data", [])
        texts = [tweet["text"] for tweet in tweets]
        return texts

    return {"error": "Platform not supported"}

def detect_trends(posts):
    """Analyze top keywords & predict future trends using AI."""
    words = [word.lower() for post in posts for word in post.split()]
    common_words = Counter(words).most_common(10)
    
    trend_predictions = trend_analyzer([word[0] for word in common_words])
    trends = [{"keyword": word[0], "trend_score": pred["score"]} for word, pred in zip(common_words, trend_predictions)]
    
    return {"trending_topics": trends}

# Example usage:
# posts = fetch_social_conversations("twitter", "AI technology")
# print(detect_trends(posts))
