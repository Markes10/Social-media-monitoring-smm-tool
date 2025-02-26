def check_negative_sentiment(db: Session):
    negative_count = db.query(SocialMediaPost).filter(SocialMediaPost.sentiment == "negative").count()
    
    if negative_count > 5:
        alert_message = f"🚨 ALERT: {negative_count} negative posts detected!"
        asyncio.create_task(broadcast_message(alert_message))
