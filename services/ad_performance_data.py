import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("smm_data.db")
cursor = conn.cursor()

def fetch_ad_performance():
    """Fetch past social media ad performance metrics"""
    query = "SELECT ad_id, impressions, clicks, conversions, cost FROM ad_campaigns"
    df = pd.read_sql_query(query, conn)
    return df

# Example usage:
# print(fetch_ad_performance().head())
