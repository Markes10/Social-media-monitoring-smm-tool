import requests

FACEBOOK_ACCESS_TOKEN = "your-facebook-access-token"
FACEBOOK_AD_ACCOUNT_ID = "your-ad-account-id"

def fetch_facebook_ads_data():
    """Fetches ad performance data from Facebook Ads API."""
    
    url = f"https://graph.facebook.com/v18.0/{FACEBOOK_AD_ACCOUNT_ID}/ads"
    params = {
        "fields": "name,impressions,clicks,conversions,cpc",
        "access_token": FACEBOOK_ACCESS_TOKEN
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "data" not in data:
        return []

    ads_data = []
    for ad in data["data"]:
        engagement_score = (ad["clicks"] + ad["conversions"]) / max(ad["impressions"], 1)
        ads_data.append({
            "ad_name": ad["name"],
            "impressions": ad["impressions"],
            "clicks": ad["clicks"],
            "conversions": ad["conversions"],
            "cost_per_click": ad["cpc"],
            "engagement_score": engagement_score
        })

    return ads_data
