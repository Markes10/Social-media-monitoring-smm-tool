from fastapi import APIRouter
from ai_customer_response import generate_response

router = APIRouter()

@router.get("/customer_support")
def customer_support(message: str):
    """Fetch AI-generated customer support response"""
    response = generate_response(message)
    return {"user_message": message, "ai_response": response}
