from fastapi import APIRouter
from analytics import fetch_competitor_metrics

router = APIRouter()

@router.get("/competitor-benchmark")
def competitor_benchmark(platform: str, brand: str, competitor: str):
    """Compare brand vs. competitor performance."""
    
    comparison = fetch_competitor_metrics(platform, brand, competitor)
    
    return {"comparison": comparison}
