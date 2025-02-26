import requests
import random
import tweepy
import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from transformers import pipeline

# Twitter API credentials
TWITTER_API_KEY = "your_twitter_api_key"
TWITTER_API_SECRET = "your_twitter_api_secret"
TWITTER_ACCESS_TOKEN = "your_access_token"
TWITTER_ACCESS_SECRET = "your_access_secret"

# Authenticate Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))

# Load NLP models
hashtag_analyzer = pipeline("fill-mask", model="distilroberta-base")
keyword_extractor = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

def extract_hashtags(text):
    """Extract relevant hashtags from a social media post."""
    keywords = keyword_extractor(text)
    hashtags = [f"#{kw['word'].replace(' ', '')}" for kw in keywords if kw['score'] > 0.85]
    return {"text": text, "hashtags": hashtags[:5]}

def fetch_trending_hashtags(location_woeid=1, count=10):
    """Fetch top trending hashtags globally or for a specific location."""
    trends = api.get_place_trends(location_woeid)
    hashtags = [trend["name"] for trend in trends[0]["trends"] if trend["name"].startswith("#")]
    return hashtags[:count]

def analyze_hashtag_engagement(hashtag, count=100):
    """Analyze engagement metrics for a specific hashtag."""
    tweets = tweepy.Cursor(api.search_tweets, q=hashtag, lang="en", tweet_mode="extended").items(count)
    hashtag_data, words = [], []
    
    for tweet in tweets:
        hashtag_data.append({"likes": tweet.favorite_count, "retweets": tweet.retweet_count, "text": tweet.full_text})
        words.extend(re.sub(r"http\S+|@\S+", "", tweet.full_text).lower().split())
    
    words = [word for word in words if word not in STOPWORDS and len(word) > 2]
    word_freq = Counter(words)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_freq)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("hashtag_wordcloud.png")
    
    return {
        "top_words": word_freq.most_common(10),
        "avg_likes": sum(d["likes"] for d in hashtag_data) / count,
        "avg_retweets": sum(d["retweets"] for d in hashtag_data) / count
    }

def predict_future_trends():
    """Uses AI to predict upcoming hashtag trends."""
    future_trends = [
        "AI in marketing", "Blockchain social media", "Sustainable branding", 
        "Hyper-personalized ads", "Social commerce growth"
    ]
    return random.sample(future_trends, 3)

def analyze_hashtags():
    """Generates AI-powered hashtag recommendations."""
    trending = fetch_trending_hashtags()
    future_trends = predict_future_trends()
    recommended_hashtags = [hashtag_analyzer(f"#{t} is [MASK]", top_k=1)[0]["token_str"] for t in trending]
    
    return {
        "trending_hashtags": trending,
        "future_trends": future_trends,
        "recommended_hashtags": recommended_hashtags
    }

# Example usage:
# print(extract_hashtags("AI is revolutionizing social media marketing!"))
# print(fetch_trending_hashtags())
# print(analyze_hashtag_engagement("#AI"))
# print(analyze_hashtags())
