import torch
import torch.nn.functional as F
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from functools import lru_cache

# Load model once at startup
MODEL_PATH = "nlp/phishing-model"

tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)
model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()


@lru_cache(maxsize=256)
def detect_message(text: str):
    """
    Detect phishing using fine-tuned transformer model
    Returns REAL phishing probability (not predicted-class confidence)
    """

    text = text.strip()

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)

    # convert logits -> probabilities
    probs = F.softmax(outputs.logits, dim=1)

    safe_prob = probs[0][0].item()
    phishing_prob = probs[0][1].item()

    label = "Phishing" if phishing_prob >= 0.5 else "Safe"

    return {
        "label": label,
        "confidence": round(phishing_prob, 4),   # always phishing probability
        "safe_probability": round(safe_prob, 4),
        "reason": "Transformer semantic analysis"
    }


