import random

trending_topics = {}

def detect_trending(topic, sentiment_score):
    """Detects trending topics based on engagement & sentiment"""
    global trending_topics
    
    if topic in trending_topics:
        trending_topics[topic]['count'] += 1
        trending_topics[topic]['sentiment'].append(sentiment_score)
    else:
        trending_topics[topic] = {'count': 1, 'sentiment': [sentiment_score]}

    # Check if topic is trending (e.g., over 50 mentions)
    if trending_topics[topic]['count'] > 50:
        avg_sentiment = sum(trending_topics[topic]['sentiment']) / len(trending_topics[topic]['sentiment'])
        return {"topic": topic, "mentions": trending_topics[topic]['count'], "sentiment": avg_sentiment}
    
    return None
