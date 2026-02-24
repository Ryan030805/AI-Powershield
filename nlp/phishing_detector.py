import torch
import torch.nn.functional as F
import time
from functools import lru_cache
from transformers import DistilBertTokenizerFast

from ai_service.amd_runtime import get_provider

# -------- ONNX LOADING --------

ONNX_PATH = "nlp/phishing-model-amd-onnx"

try:
    from optimum.onnxruntime import ORTModelForSequenceClassification

    provider = get_provider()
    print("Loading ONNX phishing model...")

    tokenizer = DistilBertTokenizerFast.from_pretrained(ONNX_PATH)

    model = ORTModelForSequenceClassification.from_pretrained(
        ONNX_PATH,
        provider=provider
    )

    USING_ONNX = True
    print("Phishing detector running on:", provider)

except Exception as e:
    print("ONNX failed -> using original PyTorch model")

    from transformers import DistilBertForSequenceClassification

    MODEL_PATH = "nlp/phishing-model"

    tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)
    model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)

    USING_ONNX = False

if not USING_ONNX:
    model.eval()



#@lru_cache(maxsize=256)
def detect_message(text: str):
    """
    Detect phishing using fine-tuned transformer model
    Returns REAL phishing probability (not predicted-class confidence)
    """

    text = text.strip()
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
    else:
        with torch.no_grad():
            outputs = model(**inputs)

    logits = outputs.logits

    # ONNX may return numpy, convert to torch tensor
    if not torch.is_tensor(logits):
        logits = torch.tensor(logits)

    probs = F.softmax(logits, dim=1)

    safe_prob = probs[0][0].item()
    phishing_prob = probs[0][1].item()

    label = "Phishing" if phishing_prob >= 0.5 else "Safe"

    latency_ms = (time.time() - start_time) * 1000

    return {
        "label": label,
        "confidence": round(phishing_prob, 4),
        "safe_probability": round(safe_prob, 4),
        "latency_ms": round(latency_ms, 2),
        "reason": "Transformer semantic analysis"
    }


