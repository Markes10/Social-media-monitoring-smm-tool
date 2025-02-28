from fastapi import APIRouter
import sqlite3
from scheduler import train_schedule_model, predict_best_time
from content_scheduler import post_scheduled_content
from celery_worker import schedule_post

router = APIRouter()

model = train_schedule_model()

@router.get("/best_posting_time")
def get_best_posting_time():
    """Predict the best time to post"""
    prediction = predict_best_time(model)
    return prediction

@router.post("/schedule_post")
def schedule_post(content: str, platform: str, scheduled_time: str):
    """Schedule a post for later"""
    conn = sqlite3.connect("smm_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scheduled_posts (content, platform, scheduled_time, status) VALUES (?, ?, ?, 'scheduled')", 
                   (content, platform, scheduled_time))
    conn.commit()
    return {"message": "Post scheduled successfully!"}

@router.post("/schedule-post")
def schedule_social_media_post(content: str, platform: str, scheduled_time: str):
    """Schedules a post for automatic publishing."""
    task = schedule_post.apply_async((content, platform, scheduled_time), eta=scheduled_time)
    return {"task_id": task.id, "status": "Post scheduled successfully!"}

@router.post("/post_now")
def post_now():
    """Trigger manual posting of scheduled content"""
    post_scheduled_content()
    return {"message": "Scheduled posts published!"}
