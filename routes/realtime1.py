from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from database import get_db
from models import SocialMediaPost
from typing import List
import smtplib

router = APIRouter()
active_connections: List[WebSocket] = []

async def broadcast_message(message: str):
    for connection in active_connections:
        await connection.send_text(message)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await broadcast_message(data)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

# Function to Check Negative Sentiment
def check_negative_sentiment(db: Session):
    negative_posts = db.query(SocialMediaPost).filter(SocialMediaPost.sentiment == "negative").count()
    if negative_posts > 5:  # Trigger alert if more than 5 negative posts are detected
        alert_message = f"🚨 ALERT: {negative_posts} negative posts detected! Take action."
        asyncio.create_task(broadcast_message(alert_message))
        send_email_alert(alert_message)

# Function to Send Email Alert
def send_email_alert(message):
    sender_email = "your-email@gmail.com"
    receiver_email = "admin@example.com"
    password = "your-email-password"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, f"Subject: Social Media Alert\n\n{message}")
    except Exception as e:
        print(f"Error sending email: {e}")
