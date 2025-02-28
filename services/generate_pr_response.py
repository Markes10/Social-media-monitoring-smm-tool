import openai

# OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key"

openai.api_key = OPENAI_API_KEY

def generate_pr_response(brand, issue, sentiment):
    """Generate AI-powered PR response based on brand crisis"""
    
    prompt = f"""
    A social media crisis has occurred for {brand}. The issue is: {issue}.
    The sentiment is {sentiment}.
    
    Generate a professional and empathetic PR response to handle this situation.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a PR expert specializing in crisis management."},
                  {"role": "user", "content": prompt}],
        max_tokens=200
    )

    return response["choices"][0]["message"]["content"]

# Example usage:
# print(generate_pr_response("Tesla", "Battery fire incident", "Negative"))
