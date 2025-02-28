import openai

openai.api_key = "your_openai_api_key"  # Replace with your API key

def generate_response(user_message):
    """Generate AI-based social media response"""
    prompt = f"User: {user_message}\nAI Brand Response:"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content'].strip()

# Example usage:
# print(generate_response("I love your product!"))
