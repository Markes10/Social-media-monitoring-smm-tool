from fastapi import APIRouter
from content_recommendation import recommend_content
from post_scheduler import suggest_post_time

router = APIRouter()

@router.get("/content-recommendation")
def get_content_recommendation():
    """Fetch AI-driven content recommendations."""
    return {"content_data": recommend_content()}

@router.get("/post-scheduler")
def get_post_schedule():
    """Fetch AI-driven post scheduling recommendation."""
    return {"schedule_data": suggest_post_time()}
