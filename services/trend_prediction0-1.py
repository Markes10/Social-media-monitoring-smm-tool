import pandas as pd
import numpy as np
import random
from transformers import pipeline
from prophet import Prophet

# AI NLP model for keyword extraction
nlp = pipeline("ner")

def train_trend_model(data):
    """Train a Facebook Prophet model to predict social media trends."""
    df = pd.DataFrame(data, columns=["date", "engagement"])
    df.rename(columns={"date": "ds", "engagement": "y"}, inplace=True)
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=30)  # Predict for next 30 days
    forecast = model.predict(future)
    return forecast[["ds", "yhat"]].tail(30).to_dict(orient="records")

def predict_trend(hashtag, historical_data):
    """Predicts future mentions of a hashtag using Prophet model."""
    df = pd.DataFrame(historical_data)
    df.rename(columns={"date": "ds", "mentions": "y"}, inplace=True)
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)
    return forecast[["ds", "yhat"]].tail(7).to_dict(orient="records")

def extract_trending_keywords(text):
    """Extracts trending keywords from social media text using NLP."""
    entities = nlp(text)
    keywords = list(set([ent["word"] for ent in entities]))
    return keywords

# Example usage:
# past_data = [{"date": "2024-02-01", "engagement": 100}, {"date": "2024-02-02", "engagement": 120}, ...]
# print(train_trend_model(past_data))
# print(predict_trend("#AI", past_data))
# print(extract_trending_keywords("AI is transforming the future of healthcare and technology!"))
