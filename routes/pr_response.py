from fastapi import APIRouter
from generate_pr_response import generate_pr_response

router = APIRouter()

@router.get("/generate_pr_response")
def fetch_pr_response(brand: str, issue: str, sentiment: str):
    """Generate AI-powered PR response"""
    return {"response": generate_pr_response(brand, issue, sentiment)}
