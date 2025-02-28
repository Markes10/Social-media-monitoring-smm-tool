import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("smm_data.db")
cursor = conn.cursor()

def fetch_engagement_data():
    """Fetch historical engagement metrics for trend prediction"""
    query = "SELECT timestamp, likes, shares, comments FROM social_media_posts"
    df = pd.read_sql_query(query, conn)

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    return df

# Example usage:
# print(fetch_engagement_data().head())
