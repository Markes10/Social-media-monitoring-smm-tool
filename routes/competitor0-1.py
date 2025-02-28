from fastapi import APIRouter
from sentiment_analysis import compare_brands
from competitor_analysis import get_competitor_data
from ai_insights import analyze_competitor

router = APIRouter()

@router.get("/competitor/comparison")
def get_competitor_analysis(brands: str, count: int = 100):
    """Compare multiple brands"""
    brand_list = brands.split(",")
    return compare_brands(brand_list, count)

@router.get("/competitor_benchmark")
def competitor_benchmark(competitor: str):
    """Fetch competitor data & AI-generated insights"""
    data = get_competitor_data(competitor)
    insights = analyze_competitor(data)
    return {"competitor_data": data, "insights": insights}
