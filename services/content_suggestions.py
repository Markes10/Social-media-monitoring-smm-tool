import openai

openai.api_key = "your_openai_api_key"

def generate_content_suggestions(topic):
    """Generate engaging social media post ideas using AI."""
    prompt = f"""
    Generate 5 engaging social media post ideas about {topic}.
    Include:
    - Captivating captions
    - Hashtags
    - Best time to post
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a social media strategist."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )

    return response['choices'][0]['message']['content'].strip()

# Example Usage:
# print(generate_content_suggestions("Eco-friendly lifestyle"))
