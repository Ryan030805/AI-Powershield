def get_provider():
    try:
        import onnxruntime as ort
        providers = ort.get_available_providers()

        if "DmlExecutionProvider" in providers:
            print("AMD/DirectML acceleration enabled")
            return "DmlExecutionProvider"
        else:
            print("DirectML not available → CPU fallback")
            return "CPUExecutionProvider"

    except Exception as e:
        print("ONNX Runtime not available → CPU fallback")
        return "CPUExecutionProvider"