from sqlalchemy.sql import func
from datetime import datetime
from database import SessionLocal
from models import SocialMediaPost

def best_posting_time(agency_id):
    """Finds the best time to post based on engagement trends."""

    db = SessionLocal()
    posts = db.query(
        func.strftime('%H', SocialMediaPost.timestamp).label("hour"),
        func.avg(SocialMediaPost.engagement_score).label("avg_engagement")
    ).filter(SocialMediaPost.agency_id == agency_id).group_by("hour").all()

    if not posts:
        return {"message": "Not enough data to determine best posting time"}

    best_hour = max(posts, key=lambda x: x.avg_engagement)
    
    return {"best_posting_hour": f"{best_hour.hour}:00"}
