from transformers import pipeline

# Load AI text generation model
text_generator = pipeline("text-generation", model="gpt2")

def generate_post(topic, tone="casual"):
    """Generate an AI-powered social media post."""
    prompt = f"Write a {tone} social media post about {topic} with trending hashtags."
    response = text_generator(prompt, max_length=50, num_return_sequences=1)
    return response[0]["generated_text"]

# Example usage:
# print(generate_post("AI in healthcare", "professional"))
