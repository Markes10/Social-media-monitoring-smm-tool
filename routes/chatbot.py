from fastapi import APIRouter
from chatbot import chatbot_response

router = APIRouter()

@router.post("/chatbot")
def chatbot_reply(message: str):
    """Generate an AI auto-reply for customer inquiries."""
    
    reply = chatbot_response(message)
    
    return {"reply": reply}
