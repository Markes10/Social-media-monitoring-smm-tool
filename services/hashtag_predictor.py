import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Connect to database
conn = sqlite3.connect("smm_data.db")

def fetch_hashtag_trends():
    """Retrieve historical hashtag engagement data"""
    query = "SELECT hashtag, posts, likes, shares, comments FROM hashtag_engagement"
    df = pd.read_sql_query(query, conn)
    return df

def train_hashtag_model():
    """Train model to predict hashtag trends"""
    df = fetch_hashtag_trends()
    
    if df.empty:
        return None
    
    X = df[['posts', 'likes', 'shares', 'comments']]
    y = df['posts'].shift(-1).fillna(0)  # Predict future post count

    model = LinearRegression()
    model.fit(X, y)
    
    return model

def predict_hashtag_performance(model, hashtag_data):
    """Predict future engagement of a hashtag"""
    X_pred = np.array([[hashtag_data['posts'], hashtag_data['likes'], hashtag_data['shares'], hashtag_data['comments']]])
    predicted_posts = model.predict(X_pred)[0]
    
    return {"predicted_posts": predicted_posts}

# Example usage:
# model = train_hashtag_model()
# if model:
#     print(predict_hashtag_performance(model, {"posts": 100, "likes": 500, "shares": 300, "comments": 200}))
