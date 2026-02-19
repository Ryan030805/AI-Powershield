import re
from PyPDF2 import PdfReader
from docx import Document
from bs4 import BeautifulSoup


#PDF Analyzer
def analyze_pdf(file_path):

    findings = []

    try:
        reader = PdfReader(file_path)

        for page in reader.pages:
            text = page.extract_text()
            if not text:
                continue

            urls = re.findall(r'https?://\S+', text)

            if urls:
                findings.append("PDF contains embedded links")

            if any(word in text.lower() for word in ["verify", "login", "account", "update", "bank"]):
                findings.append("PDF requests account verification")

            if len(text) > 50000:
                findings.append("Large document with hidden content")

    except:
        findings.append("Unable to safely parse PDF")

    return findings


#DOCX Analyzer
def analyze_docx(file_path):

    findings = []

    try:
        doc = Document(file_path)

        for rel in doc.part.rels.values():
            if "http" in rel.target_ref:
                findings.append("Document connects to external website")

    except:
        findings.append("Unable to safely parse document")

    return findings


#HTML Analyzer
def analyze_html(file_path):

    findings = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            soup = BeautifulSoup(f, "html.parser")

        forms = soup.find_all("form")
        for form in forms:
            inputs = form.find_all("input")

            for inp in inputs:
                if inp.get("type") == "password":
                    findings.append("HTML contains credential harvesting form")

        if soup.find("meta", attrs={"http-equiv": "refresh"}):
            findings.append("Page performs automatic redirect")

    except:
        findings.append("Unable to safely parse HTML")

    return findings
