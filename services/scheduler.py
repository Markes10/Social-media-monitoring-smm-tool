import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Connect to database
conn = sqlite3.connect("smm_data.db")

def fetch_engagement_data():
    """Retrieve past engagement metrics"""
    query = "SELECT time, likes, shares, comments FROM post_engagement"
    df = pd.read_sql_query(query, conn)
    return df

def train_schedule_model():
    """Train model to find best posting times"""
    df = fetch_engagement_data()

    if df.empty:
        return None

    df['hour'] = pd.to_datetime(df['time']).dt.hour
    X = df[['hour']]
    y = df[['likes', 'shares', 'comments']].sum(axis=1)  # Engagement score

    model = LinearRegression()
    model.fit(X, y)
    
    return model

def predict_best_time(model):
    """Predict best time to post"""
    hours = np.array(range(24)).reshape(-1, 1)
    predictions = model.predict(hours)
    best_hour = hours[np.argmax(predictions)][0]
    
    return {"best_posting_hour": int(best_hour)}

# Example usage:
# model = train_schedule_model()
# if model:
#     print(predict_best_time(model))
