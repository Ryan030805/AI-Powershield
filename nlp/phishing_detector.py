from transformers import pipeline
import torch
from functools import lru_cache

# Zero-shot model for phishing intent
phishing_classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# Sentiment model for emotional manipulation
sentiment_classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

# ----------------------------------
# Core detection function
# ----------------------------------

@lru_cache(maxsize=256)
def detect_message(text: str):
    """
    Phishing detection using:
    - Zero-shot intent classification
    - Sentiment analysis
    - Performance optimizations
    """

    text = text.strip()
    candidate_labels = ["phishing", "legitimate"]

    with torch.no_grad():
        phishing_result = phishing_classifier(
            text,
            candidate_labels=candidate_labels
        )

        phishing_label = phishing_result["labels"][0].upper()
        phishing_conf = float(phishing_result["scores"][0])


        if phishing_label == "PHISHING" and phishing_conf > 0.9:
            return {
                "label": "Phishing",
                "confidence": round(phishing_conf, 4),
                "reason": "High-confidence phishing intent detected",
                "details": {
                    "zero_shot": {
                        "label": phishing_label,
                        "confidence": round(phishing_conf, 4)
                    }
                }
            }

        sentiment_result = sentiment_classifier(text)[0]
        sentiment_label = sentiment_result["label"]
        sentiment_conf = float(sentiment_result["score"])

    # ----------------------------------
    # Final decision logic
    # ----------------------------------

    is_phishing = False
    reasons = []

    if phishing_label == "PHISHING" and phishing_conf > 0.7:
        is_phishing = True
        reasons.append("Zero-shot model detected phishing intent")

    if sentiment_label == "NEGATIVE" and sentiment_conf > 0.85:
        is_phishing = True
        reasons.append("Message uses fear or urgency-based language")

    if not reasons:
        reasons.append("No strong phishing indicators found")

    final_label = "Phishing" if is_phishing else "Safe"

    return {
        "label": final_label,
        "confidence": round(max(phishing_conf, sentiment_conf), 4),
        "reason": "; ".join(reasons),
        "details": {
            "zero_shot": {
                "label": phishing_label,
                "confidence": round(phishing_conf, 4)
            },
            "sentiment": {
                "label": sentiment_label,
                "confidence": round(sentiment_conf, 4)
            }
        }
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