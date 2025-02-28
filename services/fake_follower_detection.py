import numpy as np
from sklearn.ensemble import IsolationForest

def detect_fake_followers(followers, avg_likes, avg_comments):
    """Detects fake followers based on engagement rate anomalies."""
    
    data = np.array([[followers, avg_likes, avg_comments]])
    
    # Train Isolation Forest Model
    model = IsolationForest(contamination=0.1)  # Assumes 10% fake users
    model.fit(data)

    anomaly_score = model.decision_function(data)[0]
    
    # Convert score to percentage (0-100)
    fake_followers_percentage = round((1 - anomaly_score) * 100, 2)
    
    return fake_followers_percentage
