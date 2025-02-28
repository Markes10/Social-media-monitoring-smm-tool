import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("smm_data.db")
cursor = conn.cursor()

def get_ad_performance(platform):
    """Fetch ad performance metrics from the database"""
    query = """
        SELECT ad_id, impressions, clicks, conversions, cost
        FROM ad_tracking
        WHERE platform = ?
        ORDER BY conversions DESC
        LIMIT 5
    """
    cursor.execute(query, (platform,))
    data = cursor.fetchall()

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=["Ad ID", "Impressions", "Clicks", "Conversions", "Cost"])
    return df.to_dict(orient="records")

# Example usage:
# print(get_ad_performance("Facebook"))
