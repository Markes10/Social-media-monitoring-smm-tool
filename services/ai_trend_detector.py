import openai
import json

openai.api_key = "your_openai_api_key"  # Replace with your API key

def detect_trends(mentions_data):
    """Generate AI-powered insights on trending topics"""
    prompt = f"Analyze these brand mentions:\n{json.dumps(mentions_data, indent=2)}\nDetect emerging trends and suggest marketing strategies."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content'].strip()

# Example usage:
# print(detect_trends(get_brand_mentions("Apple")))
