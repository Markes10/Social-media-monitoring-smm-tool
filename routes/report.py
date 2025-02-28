from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from database import get_db
from models import SocialMediaPost

router = APIRouter()

@router.get("/generate-report")
def generate_report(db: Session = Depends(get_db)):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Social Media Analysis Report")

    # Report Header
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "Social Media Monitoring Report")

    # Sentiment Analysis Summary
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 720, "Sentiment Analysis Summary:")

    sentiment_data = db.query(SocialMediaPost.sentiment).count()
    pdf.drawString(50, 700, f"Total Posts: {sentiment_data}")

    # Top 5 Trending Hashtags
    pdf.drawString(50, 670, "Top 5 Trending Hashtags:")
    hashtags = {}
    for post in db.query(SocialMediaPost.content).all():
        words = post.content.split()
        for word in words:
            if word.startswith("#"):
                hashtags[word] = hashtags.get(word, 0) + 1
    sorted_hashtags = sorted(hashtags.items(), key=lambda x: x[1], reverse=True)[:5]

    y_pos = 650
    for tag, count in sorted_hashtags:
        pdf.drawString(50, y_pos, f"{tag}: {count} times")
        y_pos -= 20

    # Save and return PDF
    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()
