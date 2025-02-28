import tweepy

# Twitter API Credentials
API_KEY = "your_twitter_api_key"
API_SECRET = "your_twitter_api_secret"
ACCESS_TOKEN = "your_twitter_access_token"
ACCESS_SECRET = "your_twitter_access_secret"

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def post_auto_reply(tweet_id, reply_text):
    """Post AI-generated auto-reply to a tweet"""
    api.update_status(status=reply_text, in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)

# Example usage:
# post_auto_reply(123456789, "Thanks for your feedback! 😊")
