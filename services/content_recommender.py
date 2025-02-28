import sqlite3
import random

# Connect to database
conn = sqlite3.connect("smm_data.db")
cursor = conn.cursor()

def fetch_high_engagement_posts():
    """Retrieve top-performing posts for inspiration"""
    query = "SELECT post FROM competitor_posts ORDER BY likes + shares + comments DESC LIMIT 10"
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

def generate_content_ideas():
    """Generate AI-powered content suggestions"""
    high_engagement_posts = fetch_high_engagement_posts()
    
    if not high_engagement_posts:
        return ["No high-engagement posts found."]
    
    keywords = ["AI", "technology", "business", "trends", "growth"]
    content_ideas = [
        f"🔥 5 Ways {random.choice(keywords)} is Changing the World!",
        f"💡 The Future of {random.choice(keywords)}: What You Need to Know",
        f"📢 Why Your Business Should Focus on {random.choice(keywords)} in 2025"
    ]
    
    return content_ideas

# Example usage:
# print(generate_content_ideas())
