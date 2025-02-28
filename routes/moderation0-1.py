from fastapi import APIRouter
from content_moderation import is_fake_news

router = APIRouter()

moderation_queue = []  # Global moderation queue

@router.get("/get_flagged_posts")
def get_flagged_posts():
    """Return all flagged posts for admin review"""
    return {"flagged_posts": moderation_queue}

@router.get("/get_fake_news_posts")
def get_fake_news_posts():
    """Return all flagged fake news posts for admin review"""
    return {"fake_news_posts": [post for post in moderation_queue if is_fake_news(post["text"])]}

@router.post("/moderate_post")
def moderate_post(post_id: int, action: str):
    """Approve or reject a flagged post"""
    global moderation_queue
    post = next((p for p in moderation_queue if p["id"] == post_id), None)

    if not post:
        return {"error": "Post not found"}

    if action == "approve":
        approve_post(post)
    elif action == "reject":
        moderation_queue.remove(post)

    return {"status": f"Post {post_id} {action}d"}
