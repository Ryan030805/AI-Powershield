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

