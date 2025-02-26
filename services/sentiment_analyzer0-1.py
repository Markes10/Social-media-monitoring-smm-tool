import nltk
from transformers import pipeline

nltk.download("punkt")

# Load AI sentiment analysis model
sentiment_model = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    """Analyze sentiment of a given text (positive, neutral, or negative)."""
    result = sentiment_model(text)[0]
    return {"label": result["label"], "score": round(result["score"], 2)}

def detect_crisis(text):
    """Detect potential PR crisis situations based on keywords and sentiment."""
    crisis_keywords = ["scam", "fraud", "boycott", "lawsuit", "disaster", "hack", "hate"]
    sentiment = analyze_sentiment(text)
    
    if sentiment["label"] == "NEGATIVE" and any(word in text.lower() for word in crisis_keywords):
        return {"alert": True, "reason": "Potential PR crisis detected!", "sentiment": sentiment}
    
    return {"alert": False, "sentiment": sentiment}

# Example usage:
# print(analyze_sentiment("I love this brand!"))
# print(detect_crisis("This company is a scam! Avoid at all costs!"))
