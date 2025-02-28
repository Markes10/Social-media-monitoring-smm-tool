import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Sample influencer data
data = {
    "influencer": ["@fashionista_amy", "@tech_guru_john", "@fitness_mike", "@foodie_emma"],
    "followers": [50000, 120000, 75000, 90000],
    "engagement_rate": [4.5, 2.3, 6.7, 3.9],  # Percentage of engaged followers
    "bot_followers": [5, 20, 3, 10],  # Percentage of fake followers
}

df = pd.DataFrame(data)

def analyze_influencers():
    """Evaluate influencer performance & detect fake engagement."""
    
    # Normalize data for scoring
    scaler = MinMaxScaler()
    df["score"] = scaler.fit_transform(
        np.array(df["engagement_rate"] / df["bot_followers"]).reshape(-1, 1)
    )
    
    # Rank influencers based on engagement quality
    best_influencer = df.iloc[df["score"].idxmax()]
    
    return {
        "top_influencer": best_influencer["influencer"],
        "best_engagement_rate": best_influencer["engagement_rate"],
        "lowest_bot_followers": best_influencer["bot_followers"],
        "recommendation": f"Best influencer for collaboration: {best_influencer['influencer']}"
    }

# Example usage:
# print(analyze_influencers())
