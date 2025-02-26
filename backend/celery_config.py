from celery import Celery
from celery.schedules import crontab
from twitter_fetcher import fetch_twitter_data
from facebook_fetcher import fetch_facebook_data

# Initialize the Celery application
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Configure the Celery beat schedule
celery_app.conf.beat_schedule = {
    "fetch_twitter_data_every_10s": {
        "task": "twitter_fetcher.fetch_twitter_data",
        "schedule": 10.0,  # Runs every 10 seconds
    },
    "fetch_facebook_data_every_10s": {
        "task": "facebook_fetcher.fetch_facebook_data",
        "schedule": 10.0,  # Runs every 10 seconds
    },
}

# Optional: Define a task to start the Celery worker
@celery_app.task
def start_worker():
    return "Celery worker started."

if __name__ == "__main__":
    # Start the Celery worker (this line is typically run in the command line)
    print("Starting Celery worker...")