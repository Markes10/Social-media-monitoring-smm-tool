import requests
from transformers import pipeline

# Load AI model for fake news detection
fake_news_classifier = pipeline("text-classification", model="mrm8488/bert-mini-finetuned-fake-news")

def fetch_social_posts(platform, keyword):
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

def detect_fake_news(posts):
    """Analyze posts to check for misinformation."""
    results = fake_news_classifier(posts)
    
    flagged_posts = []
    for post, result in zip(posts, results):
        if result["label"] == "fake":
            flagged_posts.append({"text": post, "confidence": result["score"]})

    return {"flagged_posts": flagged_posts}

# Example usage:
# posts = fetch_social_posts("twitter", "latest news")
# print(detect_fake_news(posts))
