🛡️ AI-PowerShield
==================

AI-PowerShield is a multi-layer phishing detection and online safety platform that analyzes suspicious messages, links, and attachments using a hybrid AI + security-analysis engine.

Instead of relying on a single classifier, the system combines transformer-based language understanding with infrastructure inspection and behavioral analysis to produce interpretable security decisions and a unified risk score.

==================
AI-PowerShield does not run the transformer models directly in PyTorch during inference.

The trained DistilBERT classifiers were exported to ONNX Runtime to create a production-style inference pipeline.
ONNX converts the neural network into a compiled computation graph, allowing faster execution and lower latency on CPU hardware.

This optimization reduces response time significantly compared to standard PyTorch inference and makes the system suitable for real-time analysis.

The repository contains convert_to_onnx_amd.py, which demonstrates how the original PyTorch models were exported to ONNX format.
Users do not need to run this script — pre-exported models are provided via the download links.

⚠️ Required Model Download (Important)
======================================

The ONNX models are not included in the repository because they exceed GitHub file size limits.

Download them once before running the project.

Download Links
==============

Phishing Detection Model: https://drive.google.com/file/d/1TDF9v9ps0D20guuqutwcTYyTAc3Qh-rY/view?usp=sharing


Prompt Injection Detection Model: https://drive.google.com/file/d/1pZIBobfGN6EOe7MUStgPCdIRt-UGVhHk/view?usp=sharing


Setup Instructions
==================

1. Download both ZIP files

2. Extract them

3. Place them inside the nlp directory

🛠️ Tech Stack
==============

Frontend:

- HTML5
- CSS3
- Vanilla JavaScript

AI & Backend (Local Inference Engine):

- Python 3.10+
- FastAPI
- Uvicorn

Machine Learning & NLP:

- DistilBERT (Transformer-based phishing detection)
- HuggingFace Transformers
- PyTorch (Training Framework)
- spaCy (linguistic analysis)
- Scikit-learn
- ONNX Runtime

Security Analysis Modules:

- URL Infrastructure Analysis (tldextract, validators, WHOIS)
- Credential Exposure Detection (Regex + Luhn Algorithm)
- Behavioral Social-Engineering Detection (Hybrid NLP engine)

File Inspection:

- PyPDF2 (PDF scanning)
- python-docx (document inspection)
- BeautifulSoup (HTML form detection)

📦 Installation
================

Follow the steps below to run AI-PowerShield locally.

1. Clone the Repository
'''
        git clone https://github.com/Ryan030805/AI-PowerShield.git
        cd AI-PowerShield
'''

2. Create Virtual Environment
'''
        python -m venv venv

            Activate it:

                - Windows
                    venv\Scripts\activate

                - Mac/Linux
                    source venv/bin/activate
'''

3. Install Dependencies
'''
        pip install -r requirements.txt
'''

4. Install spaCy Language Model

            (This step is required — the project will not run without it)

            python -m spacy download en_core_web_sm

5. Download Trained Models

    Follow the instructions in the Required Model Download section at the top of this README.


🚀 How to Use
==============

1. Paste suspicious message → Text Analyzer
2. Paste URL → URL Scanner
3. Upload PDF → Attachment Analyzer


Troubleshooting
===============

Backend fails to start / model not found

Check folder placement:

        nlp/phishing-model-amd-onnx/
        nlp/prompt_model-amd-onnx/

NOT:

        nlp/phishing-model-amd-onnx/phishing-model-amd-onnx/

(Windows zip extraction commonly creates this extra nesting.)