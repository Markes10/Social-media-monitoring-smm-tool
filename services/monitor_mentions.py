import requests
import datetime
from sentiment_analysis import analyze_sentiment

SOCIAL_MEDIA_API = "your-social-media-api-url"

def fetch_social_mentions(brand, platform):
    """Fetch recent social media mentions."""
    
    url = f"{SOCIAL_MEDIA_API}/mentions?brand={brand}&platform={platform}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

def detect_crisis(brand, platform):
    """Detect crisis by analyzing recent mentions."""
    
    mentions = fetch_social_mentions(brand, platform)
    negative_count = 0
    total_mentions = len(mentions)

    for mention in mentions:
        sentiment = analyze_sentiment(mention["text"])
        if sentiment["vader_sentiment"] == "negative":
            negative_count += 1

    negative_ratio = (negative_count / total_mentions) * 100 if total_mentions else 0

    crisis_alert = negative_ratio > 40  # Crisis threshold

    return {
        "brand": brand,
        "platform": platform,
        "negative_ratio": round(negative_ratio, 2),
        "crisis_alert": crisis_alert
    }

# Example usage:
# print(detect_crisis("Nike", "Twitter"))
