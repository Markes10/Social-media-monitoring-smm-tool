from fastapi import APIRouter
import joblib
import numpy as np

router = APIRouter()

# Load the trained AI model
model = joblib.load("ad_performance_model.pkl")

@router.post("/predict-ad-performance")
def predict_ad_performance(budget: float, target_audience: int, past_ctr: float):
    """Predicts conversions based on ad budget, audience size, and CTR."""
    prediction = model.predict(np.array([[budget, target_audience, past_ctr]]))[0]
    return {"predicted_conversions": round(prediction)}
