from transformers import AutoTokenizer
import torch
import time
import os

from ai_service.amd_runtime import get_provider

# -------- ONNX LOADING --------

ONNX_PATH = "nlp/prompt_model-amd-onnx"

try:
    from optimum.onnxruntime import ORTModelForSequenceClassification

    provider = get_provider()
    print("Loading ONNX prompt injection model...")

    tokenizer = AutoTokenizer.from_pretrained(ONNX_PATH)

    model = ORTModelForSequenceClassification.from_pretrained(
        ONNX_PATH,
        provider=provider
    )

    USING_ONNX = True
    print("Prompt detector running on:", provider)

except Exception as e:
    print("ONNX failed -> using original PyTorch prompt model")

    from transformers import AutoModelForSequenceClassification

    MODEL_PATH = os.path.join(os.path.dirname(__file__), "prompt_model")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

    USING_ONNX = False

if not USING_ONNX:
    model.eval()

def detect_prompt_injection(text: str):
    """
    Returns whether a prompt injection attack is detected
    """
    start_time = time.time()

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    if USING_ONNX:
        onnx_inputs = {k: v.cpu().numpy() for k, v in inputs.items()}
        outputs = model(**onnx_inputs)

        logits = outputs.logits
        if not torch.is_tensor(logits):
            logits = torch.tensor(logits)

        probabilities = torch.softmax(logits, dim=1)

    else:
        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=1)

    attack_probability = probabilities[0][1].item()  # label 1 = attack

    latency_ms = (time.time() - start_time) * 1000

    if attack_probability > 0.90:
        return {
            "is_attack": True,
            "confidence": round(attack_probability, 3),
            "latency_ms": round(latency_ms, 2)
    }
    else:
        return {
            "is_attack": False,
            "confidence": round(attack_probability, 3),
            "latency_ms": round(latency_ms, 2)
    }