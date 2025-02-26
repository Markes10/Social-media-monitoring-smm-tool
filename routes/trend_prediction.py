from fastapi import APIRouter
from trend_prediction import train_trend_model

router = APIRouter()

@router.post("/predict-trends")
def predict_trends(data: list):
    """Predict future social media trends based on past engagement data."""
    
    predictions = train_trend_model(data)
    
    return {"predictions": predictions}
