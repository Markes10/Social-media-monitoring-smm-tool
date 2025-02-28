import tweepy
from collections import Counter

# Twitter API Credentials
API_KEY = "your_twitter_api_key"
API_SECRET = "your_twitter_api_secret"
ACCESS_TOKEN = "your_twitter_access_token"
ACCESS_SECRET = "your_twitter_access_secret"

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def fetch_top_influencers(brand_handle, limit=10):
    """Identify top influencers engaging with the brand"""
    
    mentions = api.mentions_timeline(count=200)
    influencer_counts = Counter()
    
    for tweet in mentions:
        if tweet.user.followers_count > 5000:  # Define influencer threshold
            influencer_counts[tweet.user.screen_name] += 1  

    top_influencers = influencer_counts.most_common(limit)
    
    return [{"handle": inf[0], "mentions": inf[1]} for inf in top_influencers]

# Example usage:
# print(fetch_top_influencers("Nike"))
