import smtplib
from twilio.rest import Client

# Email Configuration
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_email_password"
SMS_ACCOUNT_SID = "your_twilio_sid"
SMS_AUTH_TOKEN = "your_twilio_auth_token"

def send_email_alert(recipient, brand, percentage):
    """Send crisis email alert"""
    message = f"🚨 Crisis Alert: {brand} is experiencing {percentage}% negative sentiment spike!"
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipient, message)

def send_sms_alert(recipient, brand, percentage):
    """Send crisis SMS alert"""
    client = Client(SMS_ACCOUNT_SID, SMS_AUTH_TOKEN)
    message = f"🚨 Crisis Alert: {brand} has {percentage}% negative sentiment spike!"
    client.messages.create(to=recipient, from_="+1234567890", body=message)
