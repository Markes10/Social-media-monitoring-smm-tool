import openai

openai.api_key = "your-openai-api-key"

def chatbot_response(user_message, is_social_media=False):
    """Generate AI-powered auto-reply for either customer inquiries or social media messages."""
    
    if is_social_media:
        prompt = f"""
        You are a helpful chatbot for a brand's social media. Respond professionally to the following customer inquiry:
        
        Customer: {user_message}
        
        Chatbot:
        """
    else:
        prompt = f"""
        A customer asked: "{user_message}"
        Respond as a professional customer support agent with helpful and concise information.
        """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150
    )

    return response["choices"][0]["message"]["content"]

# Example usage:
# print(chatbot_response("What is your return policy?"))
# print(chatbot_response("Do you have discounts available?", is_social_media=True))
