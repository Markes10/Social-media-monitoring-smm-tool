import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

def predict_sentiment(brand):
    """Predict future sentiment trends"""
    df = pd.read_csv(f"{brand}_sentiment_data.csv")
    df["sentiment_score"] = df["sentiment"].map({"Positive": 1, "Neutral": 0, "Negative": -1})
    
    scaler = MinMaxScaler()
    df["sentiment_score"] = scaler.fit_transform(df["sentiment_score"].values.reshape(-1, 1))

    model = tf.keras.models.load_model(f"{brand}_sentiment_model.h5")

    last_5_days = np.array(df["sentiment_score"].values[-5:]).reshape(1, 5, 1)
    prediction = model.predict(last_5_days)
    
    predicted_score = scaler.inverse_transform(prediction)[0][0]
    
    return {
        "brand": brand,
        "predicted_sentiment_score": predicted_score,
        "sentiment_trend": "Negative" if predicted_score < 0 else "Positive" if predicted_score > 0 else "Neutral"
    }

# Example usage:
# print(predict_sentiment("Tesla"))
