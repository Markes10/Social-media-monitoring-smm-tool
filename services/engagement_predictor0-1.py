import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sentiment_analysis import analyze_sentiment

# Load Dataset (example)
df = pd.read_csv("social_media_posts.csv")  # Columns: ['text', 'likes', 'shares', 'comments']

# Feature Engineering
df["sentiment_score"] = df["text"].apply(lambda x: analyze_sentiment(x)["vader_score"])
df["engagement_score"] = df["likes"] + df["shares"] + df["comments"]

# Train Model
X = df[["sentiment_score"]]
y = df[["likes", "shares", "comments", "engagement_score"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

def predict_engagement(text):
    """Predict likes, shares & comments for a post"""
    sentiment_score = analyze_sentiment(text)["vader_score"]
    prediction = model.predict([[sentiment_score]])
    return {
        "predicted_likes": int(prediction[0][0]),
        "predicted_shares": int(prediction[0][1]),
        "predicted_comments": int(prediction[0][2]),
        "predicted_engagement": int(prediction[0][3])
    }

# Example Usage:
# print(predict_engagement("This new product is amazing!"))
