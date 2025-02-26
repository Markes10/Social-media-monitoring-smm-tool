import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_competitor_posts(url):
    """Scrape competitor social media posts (example for Twitter)."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}
    
    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.find_all("div", class_="tweet-text")  # Example: Modify for other platforms
    
    data = []
    for post in posts[:10]:  # Limit to 10 posts
        text = post.get_text()
        engagement = len(text) * 2  # Mock engagement score
        data.append({"post": text, "engagement": engagement})
    
    return data

def analyze_trending_content(posts_data):
    """Analyze engagement metrics & suggest trending content."""
    df = pd.DataFrame(posts_data)
    top_posts = df.nlargest(3, "engagement")["post"].tolist()
    return {"trending_posts": top_posts}

# Example usage:
# print(fetch_competitor_posts("https://twitter.com/CompetitorHandle"))
# print(analyze_trending_content([{"post": "New product launch!", "engagement": 500}]))
