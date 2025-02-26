import openai

OPENAI_API_KEY = "your-api-key"

def generate_post_caption(topic):
    """Generates an engaging caption for a social media post."""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a social media expert."},
            {"role": "user", "content": f"Create a catchy social media caption about {topic}."}
        ],
        api_key=OPENAI_API_KEY
    )

    return response["choices"][0]["message"]["content"]
