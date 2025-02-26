from fastapi import APIRouter
from crisis_detection import detect_crisis

router = APIRouter()

@router.get("/crisis-detection")
def get_crisis_alert():
    """Fetch AI-driven crisis detection alerts."""
    return {"crisis_data": detect_crisis()}
