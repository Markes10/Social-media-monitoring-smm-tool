import requests

FACEBOOK_ACCESS_TOKEN = "your-facebook-access-token"
PAGE_ID = "your-page-id"

def fetch_facebook_comments():
    """Fetches recent comments from a Facebook page."""
    
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/comments"
    params = {
        "fields": "from,message",
        "access_token": FACEBOOK_ACCESS_TOKEN
    }

    response = requests.get(url, params=params)
    data = response.json()

    comments = []
    if "data" in data:
        for comment in data["data"]:
            comments.append({
                "platform": "Facebook",
                "username": comment["from"]["name"],
                "comment_text": comment["message"]
            })

    return comments
