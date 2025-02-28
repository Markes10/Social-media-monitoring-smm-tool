import tweepy
import os

# Twitter API Authentication
TWITTER_BEARER_TOKEN = "your-twitter-bearer-token"
client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

def fetch_twitter_comments(keyword, max_results=10):
    """Fetches recent tweets containing the given keyword."""
    tweets = client.search_recent_tweets(query=keyword, tweet_fields=["text", "author_id"], max_results=max_results)
    
    comments = []
    if tweets.data:
        for tweet in tweets.data:
            comments.append({
                "platform": "Twitter",
                "username": tweet.author_id,
                "comment_text": tweet.text
            })
    
    return comments

def fetch_twitter_influencer(username):
    """Fetch influencer stats from Twitter."""
    user = client.get_user(username=username, user_fields=["public_metrics"])
    
    if user.data:
        followers = user.data.public_metrics["followers_count"]
        tweet_count = user.data.public_metrics["tweet_count"]
        
        tweets = client.get_users_tweets(user.data.id, tweet_fields=["public_metrics"], max_results=10)
        
        total_likes = sum(tweet.public_metrics["like_count"] for tweet in tweets.data) if tweets.data else 0
        total_retweets = sum(tweet.public_metrics["retweet_count"] for tweet in tweets.data) if tweets.data else 0
        engagement_rate = (total_likes + total_retweets) / followers if followers > 0 else 0

        return {
            "platform": "Twitter",
            "username": username,
            "followers": followers,
            "avg_likes": total_likes / len(tweets.data) if tweets.data else 0,
            "avg_comments": total_retweets / len(tweets.data) if tweets.data else 0,
            "engagement_rate": round(engagement_rate * 100, 2)
        }
    
    return None

# Example usage:
# print(fetch_twitter_comments("AI", max_results=5))
# print(fetch_twitter_influencer("elonmusk"))