import tweepy

# Twitter API Credentials
API_KEY = "your_twitter_api_key"
API_SECRET = "your_twitter_api_secret"
ACCESS_TOKEN = "your_twitter_access_token"
ACCESS_SECRET = "your_twitter_access_secret"

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def fetch_trending_topics(woeid=1):
    """Fetch trending topics and hashtags"""
    trends = api.get_place_trends(woeid)
    
    trending_data = []
    for trend in trends[0]["trends"][:10]:  
        trending_data.append({"name": trend["name"], "tweet_volume": trend["tweet_volume"]})

    return trending_data

# Example usage:
# print(fetch_trending_topics())
