import nltk
import pandas as pd
import random
from transformers import pipeline
from datetime import datetime, timedelta

nltk.download("punkt")

# Load AI model for caption generation
caption_generator = pipeline("text-generation", model="gpt2")

def suggest_best_time(posts_data):
    """Analyze past post data to find the best posting time."""
    df = pd.DataFrame(posts_data)
    df["time"] = pd.to_datetime(df["time"])
    peak_hour = df.groupby(df["time"].dt.hour)["engagement"].mean().idxmax()
    return f"{peak_hour}:00"

def generate_caption(prompt):
    """Generate AI-powered caption based on input prompt."""
    caption = caption_generator(prompt, max_length=30, num_return_sequences=1)[0]["generated_text"]
    return caption

# Example usage:
# print(suggest_best_time([{"time": "2024-02-10 14:00", "engagement": 120}, {"time": "2024-02-10 18:00", "engagement": 200}]))
# print(generate_caption("Trending AI post about technology"))
