from fastapi import APIRouter
from email_alerts import send_email_alert
from ai_trending import detect_trending
from main import active_connections

router = APIRouter()

negative_posts = []  # Store negative posts

@router.post("/subscribe_alerts")
def subscribe_alerts(email: str):
    """Send an AI-driven email alert to the user"""
    result = send_email_alert(email)
    return {"message": result}

@router.post("/analyze_topic")
async def analyze_topic(topic: str, sentiment_score: float):
    """Analyze topic and send alert if trending"""
    trending_data = detect_trending(topic, sentiment_score)
    if trending_data:
        for connection in active_connections:
            await connection.send_json(trending_data)
    
    return {"status": "Processed", "trending": trending_data}

@router.get("/get_negative_posts")
def get_negative_posts():
    """Return all detected negative sentiment posts"""
    return {"negative_posts": negative_posts}

def log_negative_post(post):
    """Store negative post for admin review"""
    negative_posts.append(post)
    return {"status": "Logged"}