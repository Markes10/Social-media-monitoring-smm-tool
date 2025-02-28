def calculate_roi(impressions, clicks, spend, conversion_rate, revenue_per_conversion=50):
    """Calculate ROI for an ad campaign."""
    conversions = (clicks * conversion_rate) / 100
    revenue = conversions * revenue_per_conversion
    roi = ((revenue - spend) / spend) * 100  # ROI Formula

    return {
        "impressions": impressions,
        "clicks": clicks,
        "spend": spend,
        "conversions": conversions,
        "revenue": revenue,
        "roi": round(roi, 2)
    }

# Example usage:
# print(calculate_roi(50000, 1500, 1200, 3.2))
