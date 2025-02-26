from fastapi import APIRouter
from auto_response import reply_to_mentions

router = APIRouter()

@router.post("/auto-response")
def auto_reply():
    """Automatically reply to social media mentions based on sentiment."""
    return reply_to_mentions()
