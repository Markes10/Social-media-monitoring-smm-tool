from fastapi import APIRouter
from crisis_detector import detect_crisis

router = APIRouter()

@router.post("/detect-crisis")
def crisis_detection(posts: list):
    """Analyze social media posts for crisis detection."""
    
    crisis_data = detect_crisis(posts)
    
    return {"crisis_data": crisis_data}
