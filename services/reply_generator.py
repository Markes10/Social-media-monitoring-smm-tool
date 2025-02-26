from transformers import pipeline

# Load AI text generation model
reply_model = pipeline("text-generation", model="gpt2")

def generate_reply(comment):
    """Generate an AI-powered reply based on the user comment."""
    prompt = f"Reply politely and professionally to this comment: {comment}"
    response = reply_model(prompt, max_length=50, num_return_sequences=1)
    return response[0]["generated_text"]

# Example usage:
# print(generate_reply("I love this product!"))
