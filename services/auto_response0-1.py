import tweepy
import openai
from sentiment_analysis import analyze_sentiment

# Twitter API credentials
TWITTER_API_KEY = "your_twitter_api_key"
TWITTER_API_SECRET = "your_twitter_api_secret"
TWITTER_ACCESS_TOKEN = "your_access_token"
TWITTER_ACCESS_SECRET = "your_access_secret"

# Authenticate Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)

# OpenAI API Key for response generation
openai.api_key = "your_openai_api_key"

def fetch_mentions(count=10):
    """Fetch recent Twitter mentions of the brand."""
    mentions = api.mentions_timeline(count=count)
    return [{"id": tweet.id, "text": tweet.text, "user": tweet.user.screen_name} for tweet in mentions]

def generate_response(post_text, sentiment):
    """Generate AI-powered response based on sentiment."""
    prompt = f"User posted: '{post_text}'. Generate a {sentiment.lower()} response professionally and politely."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful social media assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

def reply_to_mentions():
    """Fetch mentions, analyze sentiment, generate response & reply."""
    mentions = fetch_mentions()
    
    for mention in mentions:
        sentiment_result = analyze_sentiment([mention["text"]])
        sentiment = max(sentiment_result["sentiment_summary"], key=sentiment_result["sentiment_summary"].get)
        response_text = generate_response(mention["text"], sentiment)
        api.update_status(f"@{mention['user']} {response_text}", in_reply_to_status_id=mention["id"])
    
    return {"message": "Auto-replies sent successfully!"}

# Example usage:
# print(reply_to_mentions())