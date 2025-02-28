import openai
import json

openai.api_key = "your_openai_api_key"  # Replace with your API key

def suggest_influencer_partnerships(brand, influencers_data):
    """Generate AI-powered influencer collaboration insights"""
    prompt = f"Analyze this brand '{brand}' and these influencers:\n{json.dumps(influencers_data, indent=2)}\nSuggest partnership opportunities, content strategies, and expected ROI."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content'].strip()

# Example usage:
# print(suggest_influencer_partnerships("Nike", get_top_influencers("sports")))
