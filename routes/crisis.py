from fastapi import APIRouter
from crisis_detection import detect_crisis

router = APIRouter()

@router.get("/crisis")
def fetch_crisis_alert(brand: str, count: int = 100, threshold: int = 30):
    """Detect brand crisis based on negative sentiment spikes"""
    return detect_crisis(brand, count, threshold)

@router.get("/crisis-detection")
def get_crisis_alert():
    """Fetch AI-driven crisis detection alerts."""
    return {"crisis_data": detect_crisis()}
