import requests
import pandas as pd
from collections import Counter

def fetch_influencers(platform, keyword):
    """Fetch top influencers based on a keyword (example: Twitter)."""
    if platform.lower() == "twitter":
        url = f"https://api.twitter.com/2/tweets/search/recent?query={keyword}"
        headers = {"Authorization": "Bearer YOUR_TWITTER_API_KEY"}
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": "Failed to fetch data"}

        tweets = response.json().get("data", [])
        user_counts = Counter(tweet["author_id"] for tweet in tweets)
        
        influencers = [{"id": user, "mentions": count} for user, count in user_counts.most_common(10)]
        return influencers

    return {"error": "Platform not supported"}

def analyze_influencer_reach(influencer_data):
    """Analyze influencer audience reach."""
    df = pd.DataFrame(influencer_data)
    df["reach_score"] = df["mentions"] * 10  # Mock reach score calculation
    top_influencers = df.nlargest(5, "reach_score").to_dict(orient="records")
    return {"top_influencers": top_influencers}

# Example usage:
# print(fetch_influencers("twitter", "fitness"))
# print(analyze_influencer_reach([{"id": "12345", "mentions": 30}]))
