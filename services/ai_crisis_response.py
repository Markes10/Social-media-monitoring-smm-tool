import openai
import json

openai.api_key = "your_openai_api_key"  # Replace with your API key

def generate_crisis_response(negative_posts):
    """Generate AI-driven crisis management strategies"""
    if not negative_posts:
        return "No crisis detected."

    prompt = f"Recent negative posts:\n{json.dumps(negative_posts, indent=2)}\nSuggest a crisis response plan."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content'].strip()

# Example usage:
# print(generate_crisis_response(detect_crisis()))
