import torch
import nltk
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from nltk.sentiment import SentimentIntensityAnalyzer

# Load Pretrained Model
tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

# Load NLTK Sentiment Analyzer
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

def predict_sentiment(text):
    """Predict sentiment using BERT and NLTK"""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    logits = outputs.logits
    sentiment_score = torch.argmax(logits, dim=1).item()

    # Convert numeric score to sentiment label
    sentiment_labels = {0: "Very Negative", 1: "Negative", 2: "Neutral", 3: "Positive", 4: "Very Positive"}
    bert_sentiment = sentiment_labels.get(sentiment_score, "Unknown")

    # NLTK sentiment analysis
    nltk_sentiment = sia.polarity_scores(text)
    nltk_score = round(nltk_sentiment["compound"], 2)

    return {
        "bert_sentiment": bert_sentiment,
        "nltk_sentiment": nltk_sentiment,
        "nltk_score": nltk_score
    }

# Example usage:
# print(predict_sentiment("I love this new feature! It's amazing."))
