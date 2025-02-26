from fastapi import APIRouter
from celery_worker import schedule_post

router = APIRouter()

@router.post("/schedule-post")
def schedule_social_media_post(content: str, platform: str, scheduled_time: str):
    """Schedules a post for automatic publishing."""
    task = schedule_post.apply_async((content, platform, scheduled_time), eta=scheduled_time)
    return {"task_id": task.id, "status": "Post scheduled successfully!"}
