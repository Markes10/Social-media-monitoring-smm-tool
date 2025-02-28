import requests

INSTAGRAM_ACCESS_TOKEN = "your-instagram-access-token"

def fetch_instagram_influencer(username):
    """Fetch influencer stats from Instagram."""
    
    url = f"https://graph.facebook.com/v18.0/{username}?fields=followers_count,media_count,media{{like_count,comments_count}}&access_token={INSTAGRAM_ACCESS_TOKEN}"
    
    response = requests.get(url)
    data = response.json()

    if "followers_count" in data:
        followers = data["followers_count"]
        posts = data.get("media", {}).get("data", [])

        total_likes = sum(post.get("like_count", 0) for post in posts)
        total_comments = sum(post.get("comments_count", 0) for post in posts)
        engagement_rate = (total_likes + total_comments) / followers if followers > 0 else 0

        return {
            "platform": "Instagram",
            "username": username,
            "followers": followers,
            "avg_likes": total_likes / len(posts) if posts else 0,
            "avg_comments": total_comments / len(posts) if posts else 0,
            "engagement_rate": round(engagement_rate * 100, 2)
        }
    
    return None
