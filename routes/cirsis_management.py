from fastapi import APIRouter
from crisis_detection import detect_crisis
from ai_crisis_response import generate_crisis_response
from crisis_detector import detect_crisis as detect_crisis_posts

router = APIRouter()

@router.get("/crisis_detection")
def get_crisis_status(hours: int = 6, threshold: int = 30):
    """Detect social media PR crises."""
    return detect_crisis(timeframe_hours=hours, negative_threshold=threshold)

@router.get("/crisis_alert")
def crisis_alert():
    """Fetch crisis alerts and AI-driven response strategy."""
    crisis_data = detect_crisis()
    strategy = generate_crisis_response(crisis_data)
    return {"crisis_posts": crisis_data, "response_strategy": strategy}

@router.post("/detect-crisis")
def crisis_detection(posts: list):
    """Analyze social media posts for crisis detection."""
    crisis_data = detect_crisis_posts(posts)
    return {"crisis_data": crisis_data}
