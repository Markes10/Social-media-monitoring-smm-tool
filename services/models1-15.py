from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, ForeignKey, Boolean, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import datetime

class Agency(Base):
    __tablename__ = "agencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    branding_color = Column(String, default="#0000FF")

    users = relationship("User", back_populates="agency")
    subscription_plans = relationship("SubscriptionPlan", back_populates="agency")
    analytics = relationship("Analytics", back_populates="agency")
    scheduled_posts = relationship("ScheduledPost", back_populates="agency")
    social_mentions = relationship("SocialMention", back_populates="agency")
    social_media_posts = relationship("SocialMediaPost", back_populates="agency")
    content_recommendations = relationship("ContentRecommendation", back_populates="agency")
    competitor_analysis = relationship("CompetitorAnalysis", back_populates="agency")
    ad_performance = relationship("AdPerformance", back_populates="agency")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum("admin", "moderator", "user", name="user_roles"), default="user")
    agency_id = Column(Integer, ForeignKey("agencies.id"))

    agency = relationship("Agency", back_populates="users")

class SocialMediaPost(Base):
    __tablename__ = "social_media_posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    sentiment = Column(String, nullable=False)
    sentiment_score = Column(Float, default=0.0)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    agency_id = Column(Integer, ForeignKey("agencies.id"))

    agency = relationship("Agency", back_populates="social_media_posts")
    __table_args__ = (Index("idx_sentiment", "sentiment"),)

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Integer, nullable=False)
    agency_id = Column(Integer, ForeignKey("agencies.id"))

    agency = relationship("Agency", back_populates="subscription_plans")

class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    agency_id = Column(Integer, ForeignKey("agencies.id"))
    total_posts = Column(Integer, default=0)
    avg_sentiment_score = Column(Float, default=0.0)
    engagement_rate = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    agency = relationship("Agency", back_populates="analytics")

class ScheduledPost(Base):
    __tablename__ = "scheduled_posts"

    id = Column(Integer, primary_key=True, index=True)
    agency_id = Column(Integer, ForeignKey("agencies.id"))
    content = Column(String, nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    platform = Column(String, nullable=False)
    status = Column(String, default="scheduled")
    posted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    agency = relationship("Agency", back_populates="scheduled_posts")

class PostAnalytics(Base):
    __tablename__ = "post_analytics"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("scheduled_posts.id"))
    platform = Column(String, nullable=False)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    engagement_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    post = relationship("ScheduledPost")

class SocialMention(Base):
    __tablename__ = "social_mentions"

    id = Column(Integer, primary_key=True, index=True)
    agency_id = Column(Integer, ForeignKey("agencies.id"))
    platform = Column(String, nullable=False)
    mention_text = Column(Text, nullable=False)
    user_handle = Column(String, nullable=True)
    sentiment = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    agency = relationship("Agency", back_populates="social_mentions")

class ContentRecommendation(Base):
    __tablename__ = "content_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    agency_id = Column(Integer, ForeignKey("agencies.id"))
    recommended_text = Column(Text, nullable=False)
    suggested_hashtags = Column(String, nullable=False)
    best_posting_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    agency = relationship("Agency")

class CompetitorAnalysis(Base):
    __tablename__ = "competitor_analysis"

    id = Column(Integer, primary_key=True, index=True)
    agency_id = Column(Integer, ForeignKey("agencies.id"))
    competitor_name = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    total_posts = Column(Integer, nullable=False)
    avg_engagement = Column(Integer, nullable=False)
    trending_topics = Column(Text, nullable=True)
    last_checked = Column(DateTime, default=datetime.datetime.utcnow)

    agency = relationship("Agency")
