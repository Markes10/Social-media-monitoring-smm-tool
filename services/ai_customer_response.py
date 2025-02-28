import openai

openai.api_key = "your_openai_api_key"  # Replace with your API key

def generate_response(user_message):
    """Generate AI-powered customer response"""
    prompt = f"Customer message: {user_message}\nProvide a professional, helpful, and friendly response."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content'].strip()

# Example usage:
# print(generate_response("How can I track my order?"))
