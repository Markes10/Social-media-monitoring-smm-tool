from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class SocialMediaPost(Base):
    __tablename__ = "social_media_posts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True)
    username = Column(String, index=True)
    content = Column(Text)
    sentiment = Column(String)  # Positive, Negative, Neutral
    created_at = Column(DateTime, default=func.now())
