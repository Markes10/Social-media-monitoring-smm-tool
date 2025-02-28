import joblib
from profanity_check import predict
from textblob import TextBlob

# Load the trained fake news detection model
fake_news_model = joblib.load("fake_news_model.pkl")

def is_offensive(text):
    """Detects offensive language using AI models."""
    return predict([text])[0] == 1

def detect_spam(text):
    """Detects spam based on keyword patterns."""
    spam_keywords = ["free money", "click here", "subscribe now", "win a prize"]
    return any(keyword in text.lower() for keyword in spam_keywords)

def is_fake_news(text):
    """Detects fake news using a pre-trained model."""
    return fake_news_model.predict([text])[0] == 1

def analyze_text(text):
    """Analyze text for offensive language, hate speech, spam, and fake news."""
    return {
        "offensive": is_offensive(text),
        "spam": detect_spam(text),
        "fake_news": is_fake_news(text),
        "polarity": TextBlob(text).sentiment.polarity  # Sentiment Score
    }

# Example Usage:
# result = analyze_text("You are an idiot! Click here to win free money!")
# print(result)