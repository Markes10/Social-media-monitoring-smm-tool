import smtplib
import sqlite3
from email.message import EmailMessage

# Email credentials (Replace with actual credentials)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"

def fetch_trending_data():
    """Fetch the most recent trending data from the database"""
    conn = sqlite3.connect("smm_tool.db")
    query = "SELECT * FROM TrendingData ORDER BY timestamp DESC LIMIT 5"
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def send_email_alert(recipient_email):
    """Send an email alert about trending hashtags and keywords"""
    trends = fetch_trending_data()
    if not trends:
        return "No trends available."

    message_content = "🔥 **Social Media Trends Update** 🔥\n\n"
    for trend in trends:
        message_content += f"📌 Hashtag: {trend[1]} | Keyword: {trend[2]} | Sentiment: {trend[3]}\n"

    msg = EmailMessage()
    msg.set_content(message_content)
    msg["Subject"] = "🚀 Social Media Trends Alert!"
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipient_email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Email sending failed: {str(e)}"

# Test the function
print(send_email_alert("recipient@example.com"))
