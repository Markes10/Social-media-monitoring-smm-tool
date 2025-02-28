import requests

TWITTER_BEARER_TOKEN = "your-twitter-bearer-token"

def get_trending_topics(woeid=1):  # 1 = Worldwide
    """Fetch trending Twitter topics."""
    
    url = f"https://api.twitter.com/1.1/trends/place.json?id={woeid}"
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        trends = response.json()[0]["trends"]
        return [trend["name"] for trend in trends[:10]]
    
    return []

# Example usage:
# print(get_trending_topics())
