import tweepy
from sqlalchemy.orm import Session
from database import SessionLocal
from models import CompetitorAnalysis

TWITTER_API_KEY = "your-api-key"
TWITTER_API_SECRET = "your-api-secret"
TWITTER_ACCESS_TOKEN = "your-access-token"
TWITTER_ACCESS_SECRET = "your-access-secret"
TWITTER_BEARER_TOKEN = "your-twitter-bearer-token"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)
client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

def fetch_twitter_competitor_data(competitor_handle):
    """Fetches Twitter engagement data for a competitor."""
    tweets = api.user_timeline(screen_name=competitor_handle, count=50, tweet_mode="extended")
    
    if not tweets:
        return None
    
    total_engagement = sum(tweet.favorite_count + tweet.retweet_count for tweet in tweets)
    avg_engagement = total_engagement // len(tweets)
    trending_topics = [tweet.full_text[:50] for tweet in tweets[:5]]  # Extract top 5 topics

    return {
        "total_posts": len(tweets),
        "avg_engagement": avg_engagement,
        "trending_topics": trending_topics
    }

def fetch_twitter_competitor(username):
    """Fetch competitor insights from Twitter using v2 API."""
    user = client.get_user(username=username, user_fields=["public_metrics"])
    
    if user.data:
        followers = user.data.public_metrics["followers_count"]
        tweets = client.get_users_tweets(user.data.id, tweet_fields=["public_metrics"], max_results=10)
        
        total_likes = sum(tweet.public_metrics["like_count"] for tweet in tweets.data) if tweets.data else 0
        total_retweets = sum(tweet.public_metrics["retweet_count"] for tweet in tweets.data) if tweets.data else 0
        engagement_rate = (total_likes + total_retweets) / followers if followers > 0 else 0

        # Identify top tweet based on engagement
        top_tweet = max(tweets.data, key=lambda tweet: tweet.public_metrics["like_count"], default=None)
        top_tweet_url = f"https://twitter.com/{username}/status/{top_tweet.id}" if top_tweet else None

        return {
            "platform": "Twitter",
            "username": username,
            "followers": followers,
            "avg_likes": total_likes / len(tweets.data) if tweets.data else 0,
            "avg_comments": total_retweets / len(tweets.data) if tweets.data else 0,
            "engagement_rate": round(engagement_rate * 100, 2),
            "top_post": top_tweet_url
        }
    
    return None

def save_competitor_data(agency_id, competitor_handle):
    """Saves competitor insights into the database."""
    data = fetch_twitter_competitor_data(competitor_handle)
    if not data:
        return "No data available"
    
    db: Session = SessionLocal()
    competitor = CompetitorAnalysis(
        agency_id=agency_id,
        competitor_name=competitor_handle,
        platform="twitter",
        total_posts=data["total_posts"],
        avg_engagement=data["avg_engagement"],
        trending_topics=", ".join(data["trending_topics"])
    )
    db.add(competitor)
    db.commit()
    db.close()
    return "Competitor data saved!"

# Example usage:
# print(fetch_twitter_competitor("elonmusk"))
# print(save_competitor_data(1, "nasa"))
