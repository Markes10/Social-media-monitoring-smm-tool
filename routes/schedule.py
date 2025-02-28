from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ScheduledPost
from auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/schedule-post")
def schedule_post(content: str, scheduled_time: str, platform: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Schedules a social media post for a future date."""
    
    try:
        scheduled_time = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD HH:MM:SS"}

    post = ScheduledPost(
        agency_id=user.agency_id,
        content=content,
        scheduled_time=scheduled_time,
        platform=platform.lower()
    )

    db.add(post)
    db.commit()
    
    return {"message": "Post scheduled successfully", "post_id": post.id}
