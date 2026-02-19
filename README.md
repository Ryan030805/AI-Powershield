🛡️ AI-PowerShield
==================

AI-PowerShield is a multi-layer phishing detection and online safety platform that analyzes suspicious messages, links, and attachments using a hybrid AI + security-analysis engine.

Instead of relying on a single classifier, the system combines transformer-based language understanding with infrastructure inspection and behavioral analysis to produce interpretable security decisions and a unified risk score.

⚠️ Required Model Download (Important)
======================================

This repository does not include the trained AI models because they exceed GitHub’s file size limits.

You must download them once before running the project.

Download Links
==============

Phishing Detection Model: https://drive.google.com/file/d/1Zs9al8l4JkmqEGglmmW2ABuByVH1SNnf/view?usp=sharing


Prompt Injection Detection Model: https://drive.google.com/file/d/10jCPoJsCDuYOCQf36J3P8aVqCmpJZ7VL/view?usp=drive_link


Setup Instructions
==================

- Download both zip files.
- Extract them.
- Inside the project directory, create the folders:
        nlp/phishing-model/
        nlp/prompt_model/

- Move the extracted files into their respective folders.

🛠️ Tech Stack
==============

Frontend:

HTML5
CSS3
Vanilla JavaScript

AI & Backend (Local Inference Engine):

Python 3.10+
FastAPI
Uvicorn

Machine Learning & NLP:

DistilBERT (Transformer-based phishing detection)
HuggingFace Transformers
PyTorch
spaCy (linguistic analysis)
Scikit-learn

Security Analysis Modules:

URL Infrastructure Analysis (tldextract, validators, WHOIS)
Credential Exposure Detection (Regex + Luhn Algorithm)
Behavioral Social-Engineering Detection (Hybrid NLP engine)

File Inspection:

PyPDF2 (PDF scanning)
python-docx (document inspection)
BeautifulSoup (HTML form detection)

📦 Installation
================

Follow the steps below to run AI-PowerShield locally.

1. Clone the Repository
git clone https://github.com/Ryan030805/AI-PowerShield.git
cd AI-PowerShield

2. Create Virtual Environment
python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt

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