from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "prompt_model")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()  

def detect_prompt_injection(text: str):
    """
    Returns whether a prompt injection attack is detected
    """

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)

    attack_probability = probabilities[0][1].item()  # label 1 = attack

    if attack_probability > 0.90:
        return {
            "is_attack": True,
            "confidence": round(attack_probability, 3)
        }
    else:
        return {
            "is_attack": False,
            "confidence": round(attack_probability, 3)
        }