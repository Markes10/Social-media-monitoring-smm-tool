import sqlite3
import schedule
import time
from datetime import datetime
from auto_poster import post_to_social_media

# Connect to database
conn = sqlite3.connect("smm_data.db")
cursor = conn.cursor()

def fetch_scheduled_posts():
    """Retrieve posts scheduled for today"""
    query = "SELECT id, content, platform, scheduled_time FROM scheduled_posts WHERE scheduled_time >= datetime('now')"
    cursor.execute(query)
    return cursor.fetchall()

def post_scheduled_content():
    """Auto-post scheduled content"""
    posts = fetch_scheduled_posts()
    
    for post in posts:
        post_id, content, platform, scheduled_time = post
        post_to_social_media(platform, content)  # Call posting function
        
        # Mark post as published
        cursor.execute("UPDATE scheduled_posts SET status='posted' WHERE id=?", (post_id,))
        conn.commit()

# Run every minute
schedule.every(1).minutes.do(post_scheduled_content)

while True:
    schedule.run_pending()
    time.sleep(60)
