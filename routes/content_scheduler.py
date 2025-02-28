from fastapi import APIRouter
from content_suggestions import generate_content_suggestions
from content_recommendation import recommend_content
from post_scheduler import suggest_post_time
from celery_config import schedule_post
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/content_suggestions")
def get_content_suggestions(topic: str):
    """Get AI-powered content ideas."""
    return {"topic": topic, "suggestions": generate_content_suggestions(topic)}

@router.get("/content-recommendation")
def get_content_recommendation():
    """Fetch AI-driven content recommendations."""
    return {"content_data": recommend_content()}

@router.get("/post-scheduler")
def get_post_schedule():
    """Fetch AI-driven post scheduling recommendation."""
    return {"schedule_data": suggest_post_time()}

@router.post("/schedule_post")
def schedule_social_post(platform: str, content: str, minutes_later: int):
    """Schedule a social media post for a future time."""
    post_time = datetime.utcnow() + timedelta(minutes=minutes_later)
    task = schedule_post.apply_async(args=[platform, content, post_time])
    return {"status": "Scheduled", "task_id": task.id, "platform": platform, "post_time": post_time}
