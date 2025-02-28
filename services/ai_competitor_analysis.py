import openai
import json

openai.api_key = "your_openai_api_key"  # Replace with your API key

def analyze_competitor_performance(competitor_data):
    """Generate AI-driven competitor insights"""
    if not competitor_data:
        return "No competitor data available."

    prompt = f"Recent competitor data:\n{json.dumps(competitor_data, indent=2)}\nAnalyze competitor performance and suggest insights."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content'].strip()

# Example usage:
# print(analyze_competitor_performance(fetch_competitor_mentions(["@competitor1"])))
