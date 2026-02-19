import re
import spacy

nlp = spacy.load("en_core_web_sm")


def detect_otp(text):
    # 4–8 digit standalone numbers
    matches = re.findall(r'\b\d{4,8}\b', text)

    keywords = ["otp", "verification", "code", "confirm", "authenticate"]

    doc = nlp(text.lower())

    for token in doc:
        if token.text in keywords:
            if matches:
                return True, matches

    return False, []


def luhn_check(card_number):
    digits = [int(d) for d in card_number]
    checksum = 0
    reverse = digits[::-1]

    for i, digit in enumerate(reverse):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit

    return checksum % 10 == 0


def detect_card(text):
    numbers = re.findall(r'\b\d{13,16}\b', text)

    for number in numbers:
        if luhn_check(number):
            return True, number

    return False, None


def detect_cvv(text):
    if re.search(r'\b\d{3}\b', text.lower()):
        if "cvv" in text.lower():
            return True
    return False


def detect_password(text):
    password_keywords = ["password", "passcode", "login", "pin"]

    if any(word in text.lower() for word in password_keywords):
        return True

    return False


def analyze_sensitive_data(text):
    result = {
        "otp": False,
        "card": False,
        "cvv": False,
        "password": False
    }

    otp, _ = detect_otp(text)
    card, _ = detect_card(text)
    cvv = detect_cvv(text)
    password = detect_password(text)

    result["otp"] = otp
    result["card"] = card
    result["cvv"] = cvv
    result["password"] = password

    risk = any(result.values())

    return risk, result