import tweepy

# Twitter API Credentials
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_SECRET = "your_access_secret"

# Authenticate
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def post_response(tweet_id, response_text):
    """Auto-reply to a crisis tweet"""
    api.update_status(status=response_text, in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)
    return "Response posted successfully!"

# Example usage:
# print(post_response("tweet_id_here", "We're sorry to hear that. Please DM us!"))
