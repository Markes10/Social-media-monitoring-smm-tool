import openai
import json
import pandas as pd

openai.api_key = "your_openai_api_key"  # Replace with your API key

def optimize_ad_campaigns(ad_data):
    """Use AI to suggest optimizations for ad campaigns"""
    ad_json = ad_data.to_json()

    prompt = f"Here is past social media ad performance data:\n{ad_json}\nSuggest improvements to increase ROI."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content'].strip()

# Example usage:
# print(optimize_ad_campaigns(fetch_ad_performance()))
