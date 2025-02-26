import openai

OPENAI_API_KEY = "your-openai-api-key"

def generate_auto_reply(text, sentiment):
    """Generate AI-based auto-replies based on sentiment."""
    
    prompt = f"""
    A user mentioned our brand on social media:
    - User's message: "{text}"
    - Detected sentiment: {sentiment}

    Generate a professional and engaging reply based on the sentiment:
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=100
    )

    return response["choices"][0]["message"]["content"]

# Example usage:
# print(generate_auto_reply("I love this product!", "positive"))
