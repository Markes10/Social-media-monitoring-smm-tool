celery_app = Celery(
    "tasks",
    broker="redis://your-ec2-ip:6379/0",
    backend="redis://your-ec2-ip:6379/0"
)
