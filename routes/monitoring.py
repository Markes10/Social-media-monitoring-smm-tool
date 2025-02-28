from fastapi import APIRouter
from sentiment_analyzer import analyze_sentiment, detect_crisis

router = APIRouter()

@router.post("/analyze-sentiment")
def sentiment_analysis(text: str):
    """Analyze sentiment of a given text."""
    return analyze_sentiment(text)

@router.post("/detect-crisis")
def crisis_detection(text: str):
    """Detect potential PR crisis situations."""
    return detect_crisis(text)
