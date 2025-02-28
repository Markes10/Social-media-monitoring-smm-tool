import openai

# OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key"

openai.api_key = OPENAI_API_KEY

def generate_auto_reply(brand, comment, sentiment):
    """Generate an AI-powered auto-reply for a social media comment"""
    
    prompt = f"""
    A user commented on {brand}'s social media post: "{comment}".
    The sentiment is {sentiment}.
    
    Generate a friendly and professional reply in the brand’s tone.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a social media manager creating brand-appropriate replies."},
                  {"role": "user", "content": prompt}],
        max_tokens=100
    )

    return response["choices"][0]["message"]["content"]

# Example usage:
# print(generate_auto_reply("Nike", "I love these shoes!", "Positive"))
