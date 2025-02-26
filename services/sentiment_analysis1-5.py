import tweepy
import requests
import pandas as pd
import nltk
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# Twitter API credentials (Replace with your credentials)
TWITTER_API_KEY = "your_twitter_api_key"
TWITTER_API_SECRET = "your_twitter_api_secret"
TWITTER_ACCESS_TOKEN = "your_access_token"
TWITTER_ACCESS_SECRET = "your_access_secret"

# Authenticate Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Initialize sentiment analyzers
nltk.download("vader_lexicon")
vader_analyzer = SentimentIntensityAnalyzer()
bert_analyzer = pipeline("sentiment-analysis")

def fetch_twitter_posts(keyword, count=100):
    """Fetch recent tweets mentioning a keyword."""
    tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang="en", tweet_mode="extended").items(count)
    return [tweet.full_text for tweet in tweets]

def fetch_social_posts_api(platform, keyword):
    """Fetch recent social media posts using API requests."""
    if platform.lower() == "twitter":
        url = f"https://api.twitter.com/2/tweets/search/recent?query={keyword}"
        headers = {"Authorization": "Bearer YOUR_TWITTER_API_KEY"}
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": "Failed to fetch data"}

        tweets = response.json().get("data", [])
        return [tweet["text"] for tweet in tweets]
    return {"error": "Platform not supported"}

def analyze_sentiment(text):
    """Analyze sentiment using VADER & BERT"""
    vader_score = vader_analyzer.polarity_scores(text)["compound"]
    bert_result = bert_analyzer(text)[0]

    if vader_score >= 0.05:
        vader_sentiment = "Positive"
    elif vader_score <= -0.05:
        vader_sentiment = "Negative"
    else:
        vader_sentiment = "Neutral"

    return {
        "text": text,
        "vader_sentiment": vader_sentiment,
        "bert_sentiment": bert_result["label"],
        "bert_confidence": round(bert_result["score"], 2)
    }

def sentiment_summary(posts):
    """Summarize sentiment analysis results."""
    sentiments = [analyze_sentiment(post) for post in posts]
    sentiment_counts = Counter(sent["bert_sentiment"] for sent in sentiments)
    
    crisis_level = "Low"
    if sentiment_counts.get("NEGATIVE", 0) > 5:
        crisis_level = "Medium"
    if sentiment_counts.get("NEGATIVE", 0) > 10:
        crisis_level = "High"

    return {
        "sentiment_summary": sentiment_counts,
        "crisis_level": crisis_level,
        "detailed_analysis": sentiments
    }

# Example Usage:
# tweets = fetch_twitter_posts("Tesla", 50)
# print(sentiment_summary(tweets))
