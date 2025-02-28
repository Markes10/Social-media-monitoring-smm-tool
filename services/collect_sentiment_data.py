import sqlite3
from datetime import datetime
from sentiment_analysis import analyze_sentiment

# Connect to database
conn = sqlite3.connect("smm_data.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sentiment_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        topic TEXT,
        sentiment TEXT
    )
""")
conn.commit()

def store_sentiment(topic, text):
    """Analyze and store sentiment data"""
    sentiment = analyze_sentiment(text)
    timestamp = datetime.utcnow().isoformat()

    cursor.execute("INSERT INTO sentiment_history (timestamp, topic, sentiment) VALUES (?, ?, ?)",
                   (timestamp, topic, sentiment))
    conn.commit()

# Example usage:
# store_sentiment("ProductX", "I hate this product! So disappointing!")
