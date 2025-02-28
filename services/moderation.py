from transformers import pipeline

# Load a pre-trained model for content moderation
moderation_model = pipeline("text-classification", model="facebook/roberta-hate-speech-dynabench-r4-target")

def moderate_content(text):
    result = moderation_model(text)[0]
    
    if result["label"] in ["hateful", "toxic"]:
        return {"flagged": True, "reason": result["label"], "confidence": result["score"]}
    
    return {"flagged": False}
