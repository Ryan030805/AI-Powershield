from transformers import pipeline
import torch
from functools import lru_cache

# Load your fine-tuned phishing model
classifier = pipeline(
    "text-classification",
    model="nlp/phishing-model",
    tokenizer="nlp/phishing-model",
    device=0 if torch.cuda.is_available() else -1
)

@lru_cache(maxsize=256)
def detect_message(text: str):
    """
    Detect phishing using fine-tuned transformer model
    """

    text = text.strip()

    with torch.no_grad():
        result = classifier(text)[0]

    label = "Phishing" if result["label"] == "LABEL_1" else "Safe"

    return {
        "label": label,
        "confidence": round(float(result["score"]), 4),
        "reason": "Detected using fine-tuned phishing model"
    }

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# Local Testing #
"""
if __name__ == "__main__":
    samples = [
        "Your account is suspended. Click the link immediately.",
        "Hey, are we meeting tomorrow for the project discussion?",
        "Urgent! Verify your bank details now.",
        "Please find the attached report."
    ]

    for text in samples:
        print(f"Text: {text}")
        print("Result:", detect_message(text))
        print("-" * 60)
"""