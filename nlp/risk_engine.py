from nlp.phishing_detector import detect_message
from nlp.sensitive_detector import analyze_sensitive_data
from nlp.url_scanner import scan_message_for_urls


#Risk thresholds
def get_risk_level(score):
    if score >= 80:
        return "CRITICAL"
    elif score >= 60:
        return "HIGH"
    elif score >= 35:
        return "MEDIUM"
    else:
        return "LOW"


#Main Risk Engine
def evaluate_message_risk(text):

    score = 0
    reasons = []

    module_findings = {
    "url_scanner": [],
    "credential_detector": [],
    "nlp_detector": []
}

    # URL Infrastructure Analysis 
    url_risk, url_details = scan_message_for_urls(text)

    if url_risk:
        for item in url_details:
            analysis = item["analysis"]

            if analysis.get("new_domain"):
                score += 25
                reasons.append("Domain registered recently")
                module_findings["url_scanner"].append("Domain registered recently")

            if analysis.get("high_entropy"):
                score += 20
                reasons.append("Randomized domain structure")
                module_findings["url_scanner"].append("Randomized domain structure")

            if analysis.get("too_many_subdomains"):
                score += 15
                reasons.append("Excessive subdomain nesting")
                module_findings["url_scanner"].append("Excessive subdomain nesting")

            if analysis.get("keyword_stuffing"):
                score += 15
                reasons.append("Phishing keyword patterns in domain")
                module_findings["url_scanner"].append("Phishing keyword patterns in domain")

            if analysis.get("homoglyph_attack"):
                score += 25
                reasons.append("Look-alike character substitution detected")
                module_findings["url_scanner"].append("Look-alike character substitution detected")

            if analysis.get("long_domain"):
                score += 10
                reasons.append("Unusually long domain name")
                module_findings["url_scanner"].append("Unusually long domain name")

    #Credential Exposure Detection
    sensitive_risk, details = analyze_sensitive_data(text)

    if sensitive_risk:
        if details.get("otp"):
            score += 55
            reasons.append("OTP disclosure attempt")
            module_findings["credential_detector"].append("OTP disclosure attempt")

        if details.get("password"):
            score += 30
            reasons.append("Password sharing attempt")
            module_findings["credential_detector"].append("Password sharing attempt")

        if details.get("card"):
            score += 45
            reasons.append("Credit/Debit card number exposure")
            module_findings["credential_detector"].append("Credit/Debit card number exposure")

        if details.get("cvv"):
            score += 50
            reasons.append("CVV disclosure (critical financial risk)")
            module_findings["credential_detector"].append("CVV disclosure (critical financial risk)")

    # NLP Social Engineering Detection
    text_lower = text.lower()

    behavioral_flags = [
        "verify your account",
        "account suspended",
        "suspended today",
        "confirm your identity",
        "update your details",
        "login immediately",
        "unauthorized access",
        "security alert",
        "avoid suspension",
        "act now",
        "limited time",
        "failure to comply",
        "click below",
        "validate your account",
        "your account will be blocked",
        "temporary hold",
        "reactivate your account",
        "bank notice",
        "urgent action required"
    ]

    behavior_triggered = False

    for phrase in behavioral_flags:
        if phrase in text_lower:
            score += 25
            behavior_triggered = True
            reasons.append("Psychological pressure tactics detected")
            module_findings["nlp_detector"].append("Behavioral social engineering pattern")
            break
    
    result = detect_message(text)
    probability = float(result["confidence"])

    
    if probability >= 0.15:
        if behavior_triggered:
            score += probability * 30
        else:
            score += probability * 50

    if probability >= 0.60:
        reasons.append("High likelihood of social engineering")
        module_findings["nlp_detector"].append("Strong phishing language pattern")

    elif probability >= 0.30:
        reasons.append("Suspicious manipulation tone")
        module_findings["nlp_detector"].append("Moderate social engineering indicators")

    elif probability >= 0.25:
        reasons.append("Unusual persuasive communication style")
        module_findings["nlp_detector"].append("Low confidence behavioral anomaly")

    # Normalize score
    if score > 100:
        score = 100

    risk_level = get_risk_level(score)

    return {
        "risk_score": round(score, 2),
        "risk_level": risk_level,
        "reasons": list(dict.fromkeys(reasons)),
        "module_findings": module_findings
    }