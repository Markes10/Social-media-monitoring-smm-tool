import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim import corpora, models
import pandas as pd
from prophet import Prophet
from firebase_admin import messaging, credentials
import firebase_admin
import requests
import matplotlib.pyplot as plt
from sqlalchemy.sql import func
from database import SessionLocal
from models import SocialMediaPost

nltk.download("punkt")
nltk.download("stopwords")

SOCIAL_MEDIA_API = "your-social-media-api-url"

cred = credentials.Certificate("firebase-admin-sdk.json")
firebase_admin.initialize_app(cred)

def get_topics(num_topics=5, num_words=5):
    db = SessionLocal()
    posts = [post.content for post in db.query(SocialMediaPost.content).all()]

    stop_words = set(stopwords.words("english"))
    tokenized_texts = [[word.lower() for word in word_tokenize(post) if word.isalnum() and word.lower() not in stop_words] for post in posts]

    dictionary = corpora.Dictionary(tokenized_texts)
    corpus = [dictionary.doc2bow(text) for text in tokenized_texts]
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)
    topics = lda_model.print_topics(num_words=num_words)

    return [{"topic": i, "words": topic} for i, topic in enumerate(topics)]

def predict_sentiment_trends(days=7):
    db = SessionLocal()
    results = db.query(
        func.date(SocialMediaPost.timestamp).label("date"),
        SocialMediaPost.sentiment,
        func.count(SocialMediaPost.id).label("count")
    ).group_by("date", SocialMediaPost.sentiment).all()

    df = pd.DataFrame(results, columns=["date", "sentiment", "count"])
    sentiment_models = {}

    for sentiment in ["positive", "negative", "neutral"]:
        sentiment_df = df[df["sentiment"] == sentiment][["date", "count"]].rename(columns={"date": "ds", "count": "y"})

        if not sentiment_df.empty:
            model = Prophet()
            model.fit(sentiment_df)
            future = model.make_future_dataframe(periods=days)
            forecast = model.predict(future)
            sentiment_models[sentiment] = forecast[["ds", "yhat"]].to_dict(orient="records")

    return sentiment_models

def check_negative_sentiment_spike():
    db = SessionLocal()
    latest_sentiments = db.query(
        func.date(SocialMediaPost.timestamp).label("date"),
        SocialMediaPost.sentiment,
        func.count(SocialMediaPost.id).label("count")
    ).group_by("date", SocialMediaPost.sentiment).all()

    for row in latest_sentiments:
        if row.sentiment == "negative" and row.count > 50:
            send_push_notification("Negative sentiment spike detected!", f"On {row.date}, there were {row.count} negative posts.")

def send_push_notification(title, message):
    notification = messaging.Message(
        notification=messaging.Notification(title=title, body=message),
        topic="alerts"
    )
    messaging.send(notification)

def fetch_engagement_metrics(platform, brand):
    url = f"{SOCIAL_MEDIA_API}/analytics?platform={platform}&brand={brand}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}

def get_sentiment_trends(platform, brand):
    url = f"{SOCIAL_MEDIA_API}/sentiment-trends?platform={platform}&brand={brand}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}

def fetch_competitor_metrics(platform, brand, competitor):
    brand_url = f"{SOCIAL_MEDIA_API}/analytics?platform={platform}&brand={brand}"
    competitor_url = f"{SOCIAL_MEDIA_API}/analytics?platform={platform}&brand={competitor}"

    brand_data = requests.get(brand_url).json()
    competitor_data = requests.get(competitor_url).json()

    return {"brand": brand_data, "competitor": competitor_data}

def generate_insights():
    data = {
        "date": ["2025-02-01", "2025-02-02", "2025-02-03", "2025-02-04", "2025-02-05"],
        "likes": [150, 200, 250, 300, 280],
        "comments": [30, 45, 50, 60, 55],
        "shares": [20, 25, 40, 50, 45],
    }
    df = pd.DataFrame(data)
    df["engagement_score"] = df["likes"] + (df["comments"] * 2) + (df["shares"] * 3)
    avg_engagement = df["engagement_score"].mean()
    highest_engagement = df.iloc[df["engagement_score"].idxmax()]

    plt.figure(figsize=(8, 4))
    plt.plot(df["date"], df["engagement_score"], marker="o", linestyle="-", color="b")
    plt.title("Engagement Trend")
    plt.xlabel("Date")
    plt.ylabel("Engagement Score")
    plt.grid()
    plt.savefig("engagement_trend.png")
    
    return {
        "avg_engagement_score": avg_engagement,
        "highest_engagement_day": highest_engagement["date"],
        "insights": "Engagement is increasing. Continue posting similar content!"
    }
