import re
import nltk
from collections import Counter
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Download required nltk data
nltk.download("stopwords")

# Load English stopwords
stop_words = set(stopwords.words("english"))

def extract_hashtags(text):
    """Extracts hashtags from text"""
    return re.findall(r"#(\w+)", text)

def extract_keywords(text):
    """Extracts important keywords from text"""
    words = re.findall(r"\b\w+\b", text.lower())  # Tokenize words
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]  # Remove stopwords
    return filtered_words

def generate_wordcloud(text_list):
    """Generate a word cloud for keyword visualization"""
    text = " ".join(text_list)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
