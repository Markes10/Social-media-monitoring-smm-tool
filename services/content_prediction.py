import random
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Simulated past social media post data
data = {
    "word_count": np.random.randint(10, 300, 100),
    "image_count": np.random.randint(0, 5, 100),
    "hashtag_count": np.random.randint(0, 10, 100),
    "post_hour": np.random.randint(0, 24, 100),
    "engagement_score": np.random.randint(100, 10000, 100)  # Target variable
}

df = pd.DataFrame(data)

# Train a simple model to predict engagement
X = df.drop(columns=["engagement_score"])
y = df["engagement_score"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

def predict_post_performance(word_count, image_count, hashtag_count, post_hour):
    """Predicts engagement score based on input post features."""
    prediction = model.predict([[word_count, image_count, hashtag_count, post_hour]])
    return round(prediction[0])

# Example usage:
# print(predict_post_performance(150, 2, 5, 18))
