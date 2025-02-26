import tweepy
from sqlalchemy.orm import Session
from database import SessionLocal
from models import SocialMention
from sentiment_analysis import analyze_sentiment  # We'll implement this next

# Twitter API credentials
TWITTER_API_KEY = "your-api-key"
TWITTER_API_SECRET = "your-api-secret"
TWITTER_ACCESS_TOKEN = "your-access-token"
TWITTER_ACCESS_SECRET = "your-access-secret"

class TwitterStreamListener(tweepy.Stream):
    def on_status(self, status):
        """Processes incoming tweets and stores mentions."""
        db: Session = SessionLocal()

        mention = SocialMention(
            agency_id=1,  # Placeholder agency ID
            platform="twitter",
            mention_text=status.text,
            user_handle=status.user.screen_name,
            sentiment=analyze_sentiment(status.text)
        )

        db.add(mention)
        db.commit()
        db.close()

    def on_error(self, status_code):
        print(f"Error: {status_code}")
        return False

def start_twitter_listener():
    """Starts real-time monitoring of Twitter mentions."""
    stream = TwitterStreamListener(
        TWITTER_API_KEY, TWITTER_API_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
    )

    stream.filter(track=["your_brand_name"], is_async=True)
