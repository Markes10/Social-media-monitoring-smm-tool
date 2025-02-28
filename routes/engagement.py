from fastapi import APIRouter
from engagement_ai import generate_response

router = APIRouter()

@router.get("/engage")
def auto_engage(user_message: str):
    """AI-generated brand response"""
    return {"response": generate_response(user_message)}
