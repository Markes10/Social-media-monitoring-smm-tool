def check_negative_sentiment(db: Session):
    # Try fetching from Redis first
    cached_count = redis_client.get("negative_count")
    
    if cached_count:
        negative_count = int(cached_count)
    else:
        # If not cached, fetch from DB and store in Redis
        negative_count = db.query(SocialMediaPost).filter(SocialMediaPost.sentiment == "negative").count()
        redis_client.setex("negative_count", 60, negative_count)  # Cache for 1 minute

    if negative_count > 5:
        alert_message = f"🚨 ALERT: {negative_count} negative posts detected!"
        asyncio.create_task(broadcast_message(alert_message))
