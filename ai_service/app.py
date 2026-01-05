from fastapi import FastAPI
from pydantic import BaseModel
from nlp.phishing_detector import detect_message

app = FastAPI()

class MessageInput(BaseModel):
    message: str

@app.post("/analyze")
def analyze_message(data: MessageInput):
    return detect_message(data.message)
