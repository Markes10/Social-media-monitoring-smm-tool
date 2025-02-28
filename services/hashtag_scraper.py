import requests
import sqlite3

# Connect to database
conn = sqlite3.connect("smm_data.db")
cursor = conn.cursor()

def fetch_hashtag_data(hashtag):
    """Fetch hashtag engagement metrics from API"""
    url = f"https://api.socialmedia.com/hashtag/{hashtag}/engagement"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    return {}

def store_hashtag_data(hashtag, data):
    """Store hashtag engagement metrics in the database"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hashtag_engagement (
            hashtag TEXT, posts INT, likes INT, shares INT, comments INT
        )
    """)

    cursor.execute("INSERT INTO hashtag_engagement VALUES (?, ?, ?, ?, ?)", 
                   (hashtag, data['posts'], data['likes'], data['shares'], data['comments']))
    
    conn.commit()

# Example usage:
# data = fetch_hashtag_data("#AI")
# store_hashtag_data("#AI", data)
