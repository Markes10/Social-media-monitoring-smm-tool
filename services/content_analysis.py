import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("smm_data.db")
cursor = conn.cursor()

def get_top_content(platform):
    """Fetch top-performing content from the database"""
    query = """
        SELECT post_id, content, engagement, sentiment
        FROM content_performance
        WHERE platform = ?
        ORDER BY engagement DESC
        LIMIT 5
    """
    cursor.execute(query, (platform,))
    data = cursor.fetchall()

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=["Post ID", "Content", "Engagement", "Sentiment"])
    return df.to_dict(orient="records")

# Example usage:
# print(get_top_content("Twitter"))
