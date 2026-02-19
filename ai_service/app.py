from fastapi import FastAPI
from fastapi import UploadFile, File
import shutil
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from nlp.risk_engine import evaluate_message_risk
from nlp.phishing_detector import detect_message
from nlp.sensitive_detector import analyze_sensitive_data
from nlp.url_scanner import scan_message_for_urls
from nlp.attachment_scanner import analyze_pdf, analyze_docx, analyze_html

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageInput(BaseModel):
    message: str

@app.post("/predict")
async def predict(data: MessageInput):

    text = data.message

    risk_report = evaluate_message_risk(text)

    return {
        "risk_score": risk_report["risk_score"],
        "risk_level": risk_report["risk_level"],
        "reasons": risk_report["reasons"],
        "module_findings": risk_report["module_findings"]
    }

@app.post("/scan_attachment")
async def scan_attachment(file: UploadFile = File(...)):

    import os

    file_location = f"temp_{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    findings = []

    if file.filename.endswith(".pdf"):
        findings = analyze_pdf(file_location)

    elif file.filename.endswith(".docx"):
        findings = analyze_docx(file_location)

    elif file.filename.endswith(".html"):
        findings = analyze_html(file_location)

    else:
        findings = ["Unsupported file type"]


    result = {
        "filename": file.filename,
        "findings": findings,
        "risk": len(findings) > 0
    }

    if os.path.exists(file_location):
        os.remove(file_location)

    return result
