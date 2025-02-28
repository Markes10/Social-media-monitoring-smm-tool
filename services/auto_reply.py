import openai

openai.api_key = "your_openai_api_key"  # Replace with your actual API key

def generate_auto_reply(user_message, brand, sentiment=None):
    """Generate an AI-powered automated reply based on the user's message and sentiment."""
    prompt = f"""
    As the social media manager for {brand}, craft a professional and friendly reply to the following customer message:
    
    Customer: "{user_message}"
    
    """
    if sentiment:
        prompt += f"Detected sentiment: {sentiment}\n"
    
    prompt += "Your reply should address the customer's concerns, maintain a positive tone, and reflect the brand's voice."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional social media manager."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=100
    )
    
    return response['choices'][0]['message']['content'].strip()

# Example usage:
# print(generate_auto_reply("I need help with my order status", "Acme Corp"))
# print(generate_auto_reply("I love this product!", "Acme Corp", "positive"))
