import tweepy
import pandas as pd
from sentiment_analysis import analyze_sentiment

# Twitter API credentials
TWITTER_API_KEY = "your_twitter_api_key"
TWITTER_API_SECRET = "your_twitter_api_secret"
TWITTER_ACCESS_TOKEN = "your_access_token"
TWITTER_ACCESS_SECRET = "your_access_secret"

# Authenticate Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def collect_sentiment_data(brand, count=500):
    """Collect sentiment data for training"""
    tweets = tweepy.Cursor(api.search_tweets, q=brand, lang="en", tweet_mode="extended").items(count)
    
    data = []
    for tweet in tweets:
        sentiment = analyze_sentiment(tweet.full_text)
        data.append({"date": tweet.created_at, "sentiment": sentiment})
    
    df = pd.DataFrame(data)
    df.to_csv(f"{brand}_sentiment_data.csv", index=False)
    return df

# Example usage:
# collect_sentiment_data("Tesla", 500)
