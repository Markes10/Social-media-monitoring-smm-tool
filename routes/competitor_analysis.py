from fastapi import APIRouter
from competitor_monitor import fetch_competitor_mentions
from ai_competitor_analysis import analyze_competitor_performance
from analytics import fetch_competitor_metrics

router = APIRouter()

@router.get("/competitor_analysis")
def competitor_analysis(handles: str):
    """Fetch competitor analysis report"""
    competitor_list = handles.split(",")
    competitor_data = fetch_competitor_mentions(competitor_list)
    insights = analyze_competitor_performance(competitor_data)
    return {"competitor_data": competitor_data, "insights": insights}

@router.get("/competitor-benchmark")
def competitor_benchmark(platform: str, brand: str, competitor: str):
    """Compare brand vs. competitor performance."""
    comparison = fetch_competitor_metrics(platform, brand, competitor)
    return {"comparison": comparison}
