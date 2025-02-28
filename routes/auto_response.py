from fastapi import APIRouter
from auto_response import generate_response, reply_to_mentions

router = APIRouter()

@router.get("/generate_response")
def get_auto_response(issue: str):
    """Generate an AI-powered response to a social media issue"""
    return {"response": generate_response(issue)}

@router.post("/auto-response")
def auto_reply():
    """Automatically reply to social media mentions based on sentiment."""
    return reply_to_mentions()
