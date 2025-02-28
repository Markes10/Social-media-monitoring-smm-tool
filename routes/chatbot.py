from fastapi import APIRouter
from ai_chatbot import chatbot_response

router = APIRouter()

@router.post("/chat")
def chat_with_ai(query: str):
    """Chat with the AI-powered social media assistant"""
    response = chatbot_response(query)
    return {"response": response}

@router.post("/chatbot")
def chatbot_reply(message: str):
    """Generate an AI auto-reply for customer inquiries."""
    reply = chatbot_response(message)
    return {"reply": reply}
