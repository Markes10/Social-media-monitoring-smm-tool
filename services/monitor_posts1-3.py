from content_moderation import analyze_text, is_fake_news
from sentiment_analysis import analyze_sentiment
from keyword_analysis import extract_hashtags, extract_keywords
from database import save_trending_data

# Simulated Database
moderation_queue = []
published_posts = []


def process_post(post):
    """Analyze post for fake news, spam, offensive content, sentiment, and keywords."""
    analysis = analyze_text(post["text"])
    fake_news = is_fake_news(post["text"])
    sentiment = analyze_sentiment(post["text"])
    hashtags = extract_hashtags(post["text"])
    keywords = extract_keywords(post["text"])
    
    # Save sentiment and trending data
    save_trending_data(post["id"], hashtags, keywords)
    save_sentiment_data(post["id"], post["text"], sentiment)
    
    # Moderate post based on analysis
    if analysis["offensive"] or analysis["spam"] or fake_news:
        flag_post(post)  # Flag the post for admin review
    else:
        approve_post(post)  # Allow the post to be published
    
    print(f"Post ID: {post['id']} - Sentiment: {sentiment} - Hashtags: {hashtags} - Keywords: {keywords}")


def flag_post(post):
    """Flag post for admin moderation."""
    print(f"🚨 Post Flagged: {post['text']}")
    moderation_queue.append(post)


def approve_post(post):
    """Approve and publish post."""
    print(f"✅ Post Approved: {post['text']}")
    published_posts.append(post)


# Example Post Processing
sample_post = {"id": 1, "text": "AI is changing the world! #ArtificialIntelligence #Tech"}
process_post(sample_post)
