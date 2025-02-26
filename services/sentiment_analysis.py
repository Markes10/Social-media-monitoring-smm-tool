from textblob import TextBlob
from sqlalchemy.orm import Session
from models import SocialMediaPost
from database import get_db

def analyze_sentiment():
    db = next(get_db())
    posts = db.query(SocialMediaPost).filter(SocialMediaPost.sentiment == "Pending").all()

    for post in posts:
        analysis = TextBlob(post.content)
        if analysis.sentiment.polarity > 0:
            post.sentiment = "Positive"
        elif analysis.sentiment.polarity < 0:
            post.sentiment = "Negative"
        else:
            post.sentiment = "Neutral"
    
    db.commit()
    db.close()
