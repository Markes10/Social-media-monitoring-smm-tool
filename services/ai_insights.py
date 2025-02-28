import openai
import json

openai.api_key = "your_openai_api_key"  # Replace with your API key

def analyze_competitor(competitor_data):
    """Generate AI insights on competitors"""
    prompt = f"Analyze this competitor data:\n{json.dumps(competitor_data, indent=2)}\nProvide key insights & strategies."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content'].strip()

# Example usage:
# print(analyze_competitor(get_competitor_data("BrandX")))
