import schedule
import time
import requests

def post_to_social_media(platform, message, image_url=None):
    """Schedule a post to social media (Mock function)."""
    print(f"Posting to {platform}: {message} with image {image_url}")

def schedule_post(platform, message, post_time):
    """Schedule a post at a specific time."""
    schedule.every().day.at(post_time).do(post_to_social_media, platform, message)

# Example usage:
# schedule_post("Twitter", "Hello world! #AI", "14:00")
# while True:
#     schedule.run_pending()
#     time.sleep(60)
