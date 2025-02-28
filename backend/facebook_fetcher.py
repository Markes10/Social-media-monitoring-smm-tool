import facebook
import asyncio
from database import SessionLocal
from models import SocialMediaPost
from routes.realtime import broadcast_message

ACCESS_TOKEN = "YOUR_FACEBOOK_ACCESS_TOKEN"

# Facebook API Client
graph = facebook.GraphAPI(access_token=ACCESS_TOKEN, version="12.0")

# Function to Fetch Facebook Posts
async def fetch_facebook_data():
    db = SessionLocal()
    page_id = "your_page_id"  # Replace with a specific page ID

    while True:
        try:
            posts = graph.get_connections(id=page_id, connection_name="posts")
            for post in posts["data"]:
                if "message" in post:
                    new_post = SocialMediaPost(content=post["message"], sentiment="neutral")  # Add sentiment analysis
                    db.add(new_post)
                    await broadcast_message(f"📘 New Facebook Post: {post['message']}")
            
            db.commit()
        except Exception as e:
            print(f"Error fetching Facebook posts: {e}")

        await asyncio.sleep(10)  # Fetch new posts every 10 seconds
