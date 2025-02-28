import pandas as pd
import numpy as np
import nltk
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from nltk.corpus import stopwords

# Download stopwords
nltk.download("stopwords")

# Load dataset (Use a public dataset like FakeNewsNet or create your own)
df = pd.read_csv("fake_news_dataset.csv")  # Dataset should have 'text' and 'label' columns (0 = real, 1 = fake)

# Preprocess Data
stop_words = set(stopwords.words("english"))
df["text_clean"] = df["text"].apply(lambda x: " ".join([word for word in x.split() if word.lower() not in stop_words]))

# Split Data
X_train, X_test, y_train, y_test = train_test_split(df["text_clean"], df["label"], test_size=0.2, random_state=42)

# Train TF-IDF + Logistic Regression Model
model = make_pipeline(TfidfVectorizer(max_features=5000), LogisticRegression())
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "fake_news_model.pkl")

print("✅ Fake News Model Trained & Saved Successfully!")
