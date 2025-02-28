import smtplib
from twilio.rest import Client

# Email Alert Function
def send_email_alert(post_text):
    sender_email = "your_email@gmail.com"
    receiver_email = "admin@gmail.com"
    password = "your_password"

    subject = "🚨 Negative Post Alert!"
    body = f"Negative Post Detected:\n\n{post_text}"

    email_message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, email_message)

    print("📧 Email Alert Sent!")

# SMS Alert Function
def send_sms_alert(post_text):
    account_sid = "your_twilio_sid"
    auth_token = "your_twilio_auth_token"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"🚨 Negative Post Detected! 🚨\n{post_text}",
        from_="+1234567890",  # Your Twilio number
        to="+0987654321"  # Admin's phone number
    )

    print("📱 SMS Alert Sent!")

# Example Usage
# send_email_alert("This service is terrible!")
# send_sms_alert("This product is awful!")
