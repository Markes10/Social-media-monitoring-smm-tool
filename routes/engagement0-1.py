from fastapi import APIRouter
import requests
from dotenv import load_dotenv
from engagement_analysis import get_engagement_insights
from reply_generator import generate_reply

load_dotenv()
router = APIRouter()

@router.get("/engagement-analysis")
def fetch_engagement_analysis():
    """Fetch AI-powered engagement insights."""
    return get_engagement_insights()

@router.get("/fetch-engagement")
def fetch_engagement(platform: str, post_id: str):
    """Fetch engagement data for a specific post."""
    
    if platform == "twitter":
        api_url = f"https://api.twitter.com/2/tweets/{post_id}/engagement"
        headers = {"Authorization": f"Bearer {os.getenv('TWITTER_BEARER_TOKEN')}"}
        response = requests.get(api_url, headers=headers)
    
    elif platform == "facebook":
        api_url = f"https://graph.facebook.com/{post_id}/comments"
        params = {"access_token": os.getenv("FACEBOOK_ACCESS_TOKEN")}
        response = requests.get(api_url, params=params)
    
    return response.json()

@router.post("/auto-reply")
def auto_reply(platform: str, post_id: str, comment: str):
    """Generate and post an AI-powered reply to a comment."""
    reply = generate_reply(comment)
    
    if platform == "twitter":
        api_url = "https://api.twitter.com/2/tweets"
        headers = {"Authorization": f"Bearer {os.getenv('TWITTER_BEARER_TOKEN')}"}
        data = {"text": reply, "in_reply_to_status_id": post_id}
        response = requests.post(api_url, json=data, headers=headers)
    
    elif platform == "facebook":
        api_url = f"https://graph.facebook.com/{post_id}/comments"
        params = {"message": reply, "access_token": os.getenv("FACEBOOK_ACCESS_TOKEN")}
        response = requests.post(api_url, params=params)
    
    return {"reply": reply, "status": response.json()}

