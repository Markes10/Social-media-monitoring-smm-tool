from fastapi import APIRouter
from sentiment_analyzer import analyze_sentiment, process_comments
from engagement_predictor import train_engagement_model, predict_engagement
from ai_sentiment import predict_sentiment

router = APIRouter()

@router.post("/analyze_sentiment")
def analyze_text(text: str):
    """Analyze sentiment of a given text"""
    sentiment, polarity = analyze_sentiment(text)
    ai_sentiment = predict_sentiment(text)
    return {"sentiment": sentiment, "polarity": polarity, "ai_sentiment": ai_sentiment}

@router.post("/predict_engagement")
def engagement_prediction(polarity: float):
    """Predict engagement based on sentiment polarity"""
    model = train_engagement_model(fetch_past_engagement_data())
    predicted_engagement = predict_engagement(model, polarity)
    return {"predicted_engagement": predicted_engagement}