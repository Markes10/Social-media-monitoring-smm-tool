import openai
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

openai.api_key = "your-openai-api-key"

def generate_content_recommendation(brand, trend, sentiment):
    """Generate AI-powered content recommendations based on trends & sentiment."""
    prompt = f"""
    You are a social media strategist for {brand}. 
    - The current trending topic is: {trend}.
    - Audience sentiment is {sentiment}.

    Suggest 3 engaging content ideas and the best hashtags.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Sample social media engagement data
data = {
    "content_type": ["Image", "Video", "Text", "Live Stream", "Poll"],
    "average_likes": [1200, 2500, 900, 3500, 1700],
    "average_comments": [300, 800, 100, 1500, 500],
    "average_shares": [150, 600, 50, 1000, 400]
}

df = pd.DataFrame(data)

def recommend_content():
    """Recommend the best-performing content type based on engagement metrics."""
    df["engagement_score"] = (df["average_likes"] + df["average_comments"] + df["average_shares"]) / 3
    scaler = MinMaxScaler()
    df["score"] = scaler.fit_transform(df["engagement_score"].values.reshape(-1, 1))
    best_content = df.iloc[df["score"].idxmax()]
    return {
        "best_content_type": best_content["content_type"],
        "engagement_score": round(best_content["engagement_score"], 2),
        "recommendation": f"Post more {best_content['content_type']} content to maximize engagement."
    }

# Example usage:
# print(generate_content_recommendation("Nike", "AI in Sports", "Positive"))
# print(recommend_content())
