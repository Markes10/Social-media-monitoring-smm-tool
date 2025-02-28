import smtplib
from competitor_analysis import analyze_trends

def send_email_alert(subject, message, recipient):
    """Send email alerts for competitor trends"""
    sender_email = "your_email@example.com"
    sender_password = "your_email_password"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, recipient, email_message)

def send_trend_alerts():
    """Check trends & send alerts"""
    trends = analyze_trends()
    message = f"🚀 Trending Competitor Hashtags:\n{trends}"
    send_email_alert("📊 Competitor Trend Alert", message, "your_email@example.com")

# Example usage:
# send_trend_alerts()
