import requests
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from dotenv import load_dotenv

load_dotenv()

# Facebook Ads API Setup
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
FACEBOOK_AD_ACCOUNT_ID = os.getenv("FACEBOOK_AD_ACCOUNT_ID")

def fetch_facebook_ads():
    """Fetch Facebook Ad performance metrics."""
    url = f"https://graph.facebook.com/v15.0/{FACEBOOK_AD_ACCOUNT_ID}/insights"
    params = {
        "access_token": FACEBOOK_ACCESS_TOKEN,
        "fields": "impressions,clicks,spend,conversion_rate",
        "date_preset": "last_30d"
    }
    response = requests.get(url, params=params)
    return response.json()

def fetch_google_ads():
    """Mock function to fetch Google Ads data."""
    return {
        "impressions": 50000,
        "clicks": 1500,
        "spend": 1200,
        "conversion_rate": 3.2
    }

def fetch_twitter_ads():
    """Mock function to fetch Twitter Ads data."""
    return {
        "impressions": 30000,
        "clicks": 800,
        "spend": 900,
        "conversion_rate": 2.5
    }

# Sample ad performance data
data = {
    "campaign": ["Ad Campaign A", "Ad Campaign B", "Ad Campaign C", "Ad Campaign D"],
    "click_through_rate": [2.1, 3.5, 1.8, 4.2],  # CTR in %
    "cost_per_click": [0.50, 0.40, 0.60, 0.35],  # CPC in $
    "conversion_rate": [1.2, 2.8, 0.9, 3.5],  # Conversion rate in %
    "budget": [1000, 2000, 1500, 2500],  # Ad budget in $
}

df = pd.DataFrame(data)

def optimize_ad_performance():
    """Evaluate ad campaigns & suggest improvements."""
    df["ad_score"] = (df["click_through_rate"] * df["conversion_rate"]) / df["cost_per_click"]
    scaler = MinMaxScaler()
    df["score"] = scaler.fit_transform(df["ad_score"].values.reshape(-1, 1))
    best_ad = df.iloc[df["score"].idxmax()]
    return {
        "best_campaign": best_ad["campaign"],
        "best_ctr": best_ad["click_through_rate"],
        "best_cpc": best_ad["cost_per_click"],
        "best_conversion_rate": best_ad["conversion_rate"],
        "recommendation": f"Increase budget for {best_ad['campaign']} for better ROI."
    }

# Example usage:
# print(fetch_facebook_ads())
# print(fetch_google_ads())
# print(fetch_twitter_ads())
# print(optimize_ad_performance())
