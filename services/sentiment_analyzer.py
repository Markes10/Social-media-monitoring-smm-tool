import sqlite3
import pandas as pd
import nltk
from textblob import TextBlob
from transformers import pipeline

# Download necessary NLP resources
nltk.download("punkt")

# Connect to database
conn = sqlite3.connect("smm_data.db")
cursor = conn.cursor()

# Load AI sentiment analysis model
sentiment_model = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    """Analyze sentiment using both TextBlob and transformers."""
    blob_analysis = TextBlob(text)
    polarity = blob_analysis.sentiment.polarity
    bert_result = sentiment_model(text)[0]
    
    if polarity > 0:
        textblob_sentiment = "Positive"
    elif polarity < 0:
        textblob_sentiment = "Negative"
    else:
        textblob_sentiment = "Neutral"
    
    return {
        "textblob_sentiment": textblob_sentiment,
        "textblob_polarity": polarity,
        "bert_sentiment": bert_result["label"],
        "bert_confidence": round(bert_result["score"], 2)
    }

def detect_crisis(text):
    """Detect potential PR crisis situations based on keywords and sentiment."""
    crisis_keywords = ["scam", "fraud", "boycott", "lawsuit", "disaster", "hack", "hate"]
    sentiment = analyze_sentiment(text)
    
    if sentiment["bert_sentiment"].upper() == "NEGATIVE" and any(word in text.lower() for word in crisis_keywords):
        return {"alert": True, "reason": "Potential PR crisis detected!", "sentiment": sentiment}
    
    return {"alert": False, "sentiment": sentiment}

def process_comments():
    """Analyze sentiment of recent comments and update the database."""
    query = "SELECT id, comment_text FROM comments WHERE sentiment IS NULL"
    df = pd.read_sql_query(query, conn)

    for index, row in df.iterrows():
        sentiment = analyze_sentiment(row['comment_text'])
        cursor.execute("UPDATE comments SET sentiment=?, polarity=? WHERE id=?", 
                       (sentiment["bert_sentiment"], sentiment["textblob_polarity"], row['id']))
    
    conn.commit()

# Example Usage:
# process_comments()
# print(detect_crisis("This company is a scam! Avoid at all costs!"))
