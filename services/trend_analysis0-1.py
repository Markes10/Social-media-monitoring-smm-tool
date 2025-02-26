import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

# Twitter API authentication
auth = tweepy.OAuthHandler(os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_SECRET"))
api = tweepy.API(auth)

def get_trending_hashtags(woeid=1):  # WOEID 1 = Worldwide
    """Fetch trending Twitter hashtags."""
    trends = api.get_place_trends(id=woeid)
    return [trend["name"] for trend in trends[0]["trends"]]

# Example usage:
# print(get_trending_hashtags())
