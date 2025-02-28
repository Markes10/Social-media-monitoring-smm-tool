import openai
import json

openai.api_key = "your_openai_api_key"  # Replace with your API key

def recommend_collaborations(influencer_data):
    """Generate AI-powered partnership recommendations"""
    prompt = f"Analyze these influencers:\n{json.dumps(influencer_data, indent=2)}\nSuggest collaboration strategies, content ideas, and expected ROI."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content'].strip()

# Example usage:
# print(recommend_collaborations(get_top_influencers("Tech")))
