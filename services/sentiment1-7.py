import sqlite3
import pandas as pd
import nltk
import openai
import threading
import time
from textblob import TextBlob
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from alert_system import send_email_alert, send_sms_alert

# Initialize sentiment models
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()
bert_sentiment = pipeline("sentiment-analysis")

# OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key"
openai.api_key = OPENAI_API_KEY

# Connect to the database
conn = sqlite3.connect("smm_data.db")
cursor = conn.cursor()

def analyze_sentiment(text):
    """Analyze sentiment using multiple models."""
    vader_score = sia.polarity_scores(text)['compound']
    textblob_score = TextBlob(text).sentiment.polarity
    bert_result = bert_sentiment(text)[0]
    openai_prompt = f"Analyze sentiment: \"{text}\" as Positive, Neutral, or Negative."
    openai_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert in sentiment analysis."},
                  {"role": "user", "content": openai_prompt}],
        max_tokens=20
    )

    return {
        "vader_sentiment": "positive" if vader_score > 0 else "negative" if vader_score < 0 else "neutral",
        "vader_score": vader_score,
        "textblob_score": textblob_score,
        "bert_sentiment": bert_result["label"].lower(),
        "bert_confidence": bert_result["score"],
        "openai_sentiment": openai_response["choices"][0]["message"]["content"].strip()
    }

def detect_crisis():
    """Detect potential PR crisis based on negative sentiment spikes."""
    query = "SELECT post_id, content FROM social_media_posts ORDER BY timestamp DESC LIMIT 100"
    cursor.execute(query)
    posts = cursor.fetchall()
    
    negative_posts = [post for post in posts if analyze_sentiment(post[1])["vader_score"] < -0.3]
    return negative_posts if len(negative_posts) > 10 else []

def monitor_posts():
    """Continuously check posts for negative sentiment and send alerts."""
    while True:
        query = "SELECT id, text FROM posts WHERE processed = 0"
        cursor.execute(query)
        posts = cursor.fetchall()
        
        for post in posts:
            sentiment = analyze_sentiment(post[1])
            if sentiment["vader_sentiment"] == "negative":
                send_alert(post)
            cursor.execute("UPDATE posts SET processed = 1 WHERE id = ?", (post[0],))
        conn.commit()
        time.sleep(5)

def send_alert(post):
    """Send an alert via email & SMS when negative sentiment is found."""
    print(f"🚨 ALERT: Negative Post Detected!\nID: {post[0]} | Text: {post[1]}\n")
    send_email_alert(post[1])
    send_sms_alert(post[1])

def compare_brands(brand_list, count=100):
    """Compare sentiment & engagement metrics for multiple brands."""
    results = {}
    for brand in brand_list:
        query = "SELECT content FROM social_media_posts WHERE brand = ? ORDER BY timestamp DESC LIMIT ?"
        cursor.execute(query, (brand, count))
        posts = cursor.fetchall()
        sentiments = [analyze_sentiment(post[0]) for post in posts]
        positive_count = sum(1 for s in sentiments if s["vader_sentiment"] == "positive")
        negative_count = sum(1 for s in sentiments if s["vader_sentiment"] == "negative")
        neutral_count = count - (positive_count + negative_count)
        results[brand] = {
            "sentiment_distribution": {
                "Positive": positive_count,
                "Negative": negative_count,
                "Neutral": neutral_count
            }
        }
    return results

# Start monitoring in a separate thread
threading.Thread(target=monitor_posts, daemon=True).start()

# Example Usage:
# print(analyze_sentiment("This product is amazing!"))
# print(compare_brands(["Tesla", "Ford", "BMW"], 50))
