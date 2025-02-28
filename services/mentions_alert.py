import smtplib
from email.message import EmailMessage
from sqlalchemy.orm import Session
from database import SessionLocal
from models import SocialMention

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "your-email@gmail.com"
EMAIL_PASS = "your-password"

def send_email_alert(to_email, mention):
    """Sends an email alert for negative mentions."""
    
    msg = EmailMessage()
    msg["Subject"] = "🚨 Negative Brand Mention Detected!"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg.set_content(f"Your brand was mentioned negatively on {mention.platform}:\n\n{mention.mention_text}\n\nUser: {mention.user_handle}")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

def check_for_negative_mentions():
    """Checks for negative mentions and sends alerts."""
    
    db: Session = SessionLocal()
    mentions = db.query(SocialMention).filter(SocialMention.sentiment == "negative").all()

    for mention in mentions:
        send_email_alert("admin@example.com", mention)

    db.close()
