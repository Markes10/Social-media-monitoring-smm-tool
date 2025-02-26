def predict_engagement(likes, shares, comments, impressions):
    """Predicts engagement score based on post metrics."""
    
    model = train_engagement_model()
    if not model:
        return "Not enough data to predict engagement"

    features = np.array([[likes, shares, comments, impressions]])
    prediction = model.predict(features)

    return round(prediction[0], 2)
