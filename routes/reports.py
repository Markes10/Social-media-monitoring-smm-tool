from fastapi import APIRouter
from report_generator import generate_report

router = APIRouter()

@router.get("/generate_report")
def get_report():
    """Trigger the AI-powered social media report generation"""
    report_path = generate_report()
    return {"message": "Report generated successfully!", "report_url": report_path}
