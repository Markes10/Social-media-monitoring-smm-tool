import openai
import spacy

# Load the spaCy model for natural language processing
nlp = spacy.load("en_core_web_sm")

# Set your OpenAI API key
openai.api_key = "your-openai-api-key"  # Replace with your OpenAI API key

def generate_post_suggestions(agency_name, category):
    """Generates AI-powered post ideas based on agency category."""
    
    prompt = f"Generate 3 creative and engaging social media post ideas for a {category} brand named {agency_name}."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150
    )

    return response["choices"][0]["message"]["content"]

def recommend_hashtags(post_content):
    """Extracts keywords from a post and suggests hashtags."""
    
    doc = nlp(post_content)
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN", "ADJ"]]
    
    hashtags = [f"#{word.lower()}" for word in keywords[:5]]  # Limit to top 5
    return " ".join(hashtags)

def generate_social_media_post(topic, audience, platform):
    """Generates AI-driven post recommendations."""
    
    prompt = f"Create an engaging {platform} post about {topic} targeting {audience}. Include hashtags and a call to action."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=100
    )

    return response["choices"][0]["message"]["content"]

# Example usage:
if __name__ == "__main__":
    # Generate post suggestions for an agency
    agency_name = "EcoAgency"
    category = "sustainability"
    print("Post Suggestions:")
    print(generate_post_suggestions(agency_name, category))

    # Generate a social media post
    topic = "Eco-friendly living"
    audience = "millennials"
    platform = "Instagram"
    post_content = generate_social_media_post(topic, audience, platform)
    print("\nGenerated Social Media Post:")
    print(post_content)

    # Recommend hashtags for the generated post
    hashtags = recommend_hashtags(post_content)
    print("\nRecommended Hashtags:")
    print(hashtags)