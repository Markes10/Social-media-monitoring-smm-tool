import openai
import json

openai.api_key = "your_openai_api_key"  # Replace with your API key

def optimize_content(content_data):
    """Generate AI-based content improvement suggestions"""
    prompt = f"Analyze this top-performing content:\n{json.dumps(content_data, indent=2)}\nSuggest content improvements & engagement strategies."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content'].strip()

# Example usage:
# print(optimize_content(get_top_content("Instagram")))
