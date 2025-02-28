def generate_pr_response(negative_mentions):
    """Generate AI-based PR response strategy"""
    if negative_mentions < 10:
        return "Monitor the situation, no major action needed."
    elif 10 <= negative_mentions < 30:
        return "Acknowledge concerns on social media & clarify any misinformation."
    else:
        return "Issue an official brand statement & activate crisis management team."

# Example usage:
# print(generate_pr_response(25))
