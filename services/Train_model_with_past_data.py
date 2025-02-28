import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Load past post data
df = pd.read_csv("social_media_posts.csv")  # Columns: [text, hashtags, time_posted, likes, shares, comments]

# Feature Engineering
df["text_length"] = df["text"].apply(len)

# Split Data
X = df[["text_length"]]  # Add more features later
y = df[["likes", "shares", "comments"]]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train Model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save Model
import joblib
joblib.dump(model, "engagement_predictor.pkl")
