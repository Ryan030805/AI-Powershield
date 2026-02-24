from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer

def convert(input_path, output_path):
    print(f"Converting {input_path} → ONNX")

    model = ORTModelForSequenceClassification.from_pretrained(
        input_path,
        export=True
    )

    tokenizer = AutoTokenizer.from_pretrained(input_path)

    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)

    print(f"Saved at {output_path}\n")


convert("nlp/phishing-model-amd", "nlp/phishing-model-amd-onnx")
convert("nlp/prompt_model-amd", "nlp/prompt_model-amd-onnx")

print("AMD ONNX models ready.")