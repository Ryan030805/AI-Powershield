AI PowerShield — Phishing Detection

 - AI PowerShield is an AI-powered web application that detects phishing attempts in SMS, emails, and text messages using machine learning.

AI Model

 - The phishing detection model was fine-tuned using DistilBERT on a curated dataset of phishing and legitimate messages.
    [Model weights are excluded from the repository due to size constraints.]

    ### Model Weights
    Download the fine-tuned phishing detection model:
        [https://drive.google.com/file/d/1zdpY6TZ8T5OZZDufLndvth8eun3CBCPl/view?usp=sharing]

    After downloading, extract the zip and place the folder inside:
    nlp/phishing-model/

Tech Stack

    -Language: Python
    -AI / NLP: Hugging Face Transformers (DistilBERT)
    -Backend: FastAPI
    -Frontend: HTML, CSS, JavaScript
    -Training: Google Colab