import requests

INSTAGRAM_ACCESS_TOKEN = "your-instagram-access-token"

def fetch_instagram_competitor(username):
    """Fetch competitor insights from Instagram."""
    
    url = f"https://graph.facebook.com/v18.0/{username}?fields=followers_count,media{{like_count,comments_count,permalink}}&access_token={INSTAGRAM_ACCESS_TOKEN}"
    
    response = requests.get(url)
    data = response.json()

    if "followers_count" in data:
        followers = data["followers_count"]
        posts = data.get("media", {}).get("data", [])

        total_likes = sum(post.get("like_count", 0) for post in posts)
        total_comments = sum(post.get("comments_count", 0) for post in posts)
        engagement_rate = (total_likes + total_comments) / followers if followers > 0 else 0

        # Identify top post based on engagement
        top_post = max(posts, key=lambda post: post.get("like_count", 0), default=None)
        top_post_url = top_post.get("permalink") if top_post else None

        return {
            "platform": "Instagram",
            "username": username,
            "followers": followers,
            "avg_likes": total_likes / len(posts) if posts else 0,
            "avg_comments": total_comments / len(posts) if posts else 0,
            "engagement_rate": round(engagement_rate * 100, 2),
            "top_post": top_post_url
        }
    
    return None
