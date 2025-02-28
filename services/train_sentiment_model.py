import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# Load data
brand = "Tesla"
df = pd.read_csv(f"{brand}_sentiment_data.csv")
df["sentiment_score"] = df["sentiment"].map({"Positive": 1, "Neutral": 0, "Negative": -1})
df["date"] = pd.to_datetime(df["date"])
df.sort_values("date", inplace=True)

# Normalize data
scaler = MinMaxScaler()
df["sentiment_score"] = scaler.fit_transform(df["sentiment_score"].values.reshape(-1, 1))

# Prepare training data
X, y = [], []
window_size = 5  # Use last 5 days for prediction
for i in range(len(df) - window_size):
    X.append(df["sentiment_score"].values[i:i+window_size])
    y.append(df["sentiment_score"].values[i+window_size])

X, y = np.array(X), np.array(y)

# Build LSTM model
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(window_size, 1)),
    LSTM(50),
    Dense(1)
])

model.compile(optimizer="adam", loss="mean_squared_error")
model.fit(X, y, epochs=20, batch_size=8)

# Save model
model.save(f"{brand}_sentiment_model.h5")
