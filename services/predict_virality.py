import openai

# OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key"
openai.api_key = OPENAI_API_KEY

def predict_virality(content, engagement_metrics):
    """Predict the virality of a social media post"""

    prompt = f"""
    A social media post has the following details:
    Content: "{content}"
    Engagement Metrics: {engagement_metrics}
    
    Predict if this post is likely to go viral and why.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a social media analyst predicting viral trends."},
                  {"role": "user", "content": prompt}],
        max_tokens=150
    )

    return response["choices"][0]["message"]["content"]

# Example usage:
# print(predict_virality("Check out our latest sneakers! #Nike #JustDoIt", {"likes": 500, "shares": 200}))
