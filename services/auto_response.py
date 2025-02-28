import openai

# OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key"
openai.api_key = OPENAI_API_KEY

def generate_response(issue):
    """Generate a professional crisis response"""

    prompt = f"""
    A customer has raised the following complaint on social media:
    "{issue}"

    As the brand’s PR manager, craft a professional, empathetic, and reassuring response.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a PR expert handling customer complaints."},
                  {"role": "user", "content": prompt}],
        max_tokens=100
    )

    return response["choices"][0]["message"]["content"]

# Example usage:
# print(generate_response("Your service is terrible!"))
