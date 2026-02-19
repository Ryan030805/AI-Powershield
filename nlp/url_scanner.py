import re
import math
import tldextract
import validators
import whois
from datetime import datetime


SUSPICIOUS_KEYWORDS = [
    "verify", "secure", "update", "login",
    "account", "bank", "confirm", "support"
]


#Extract URLs
def extract_urls(text):
    pattern = r'(https?://[^\s]+)'
    return re.findall(pattern, text)



def shannon_entropy(domain):
    prob = [float(domain.count(c)) / len(domain) for c in set(domain)]
    entropy = -sum(p * math.log2(p) for p in prob)
    return entropy


# Domain Age 
def get_domain_age(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date:
            return (datetime.now() - creation_date).days
    except Exception:
        return None

    return None


# Structural deception detection 
def structural_domain_analysis(domain):
    result = {
        "long_domain": False,
        "many_hyphens": False,
        "keyword_stuffing": False,
        "homoglyph_attack": False
    }

    # long domains
    if len(domain) > 22:
        result["long_domain"] = True

    # too many hyphens
    if domain.count('-') >= 3:
        result["many_hyphens"] = True

    # phishing keywords
    for word in SUSPICIOUS_KEYWORDS:
        if word in domain:
            result["keyword_stuffing"] = True
            break

    # homoglyph tricks
    homoglyph_patterns = ["0", "1", "rn", "vv", "@"]
    for pattern in homoglyph_patterns:
        if pattern in domain:
            result["homoglyph_attack"] = True
            break

    return result


# URL Analysis
def analyze_url(url):
    result = {
        "new_domain": False,
        "high_entropy": False,
        "too_many_subdomains": False,
        "domain_age_days": None,
        "entropy_score": None,
        "long_domain": False,
        "many_hyphens": False,
        "keyword_stuffing": False,
        "homoglyph_attack": False
    }

    if not validators.url(url):
        return result

    extracted = tldextract.extract(url)

    domain = extracted.domain
    suffix = extracted.suffix
    subdomain = extracted.subdomain

    full_domain = f"{domain}.{suffix}"

    # domain age
    age = get_domain_age(full_domain)
    result["domain_age_days"] = age

    if age is not None and age < 180:
        result["new_domain"] = True

    # entropy
    entropy = shannon_entropy(domain)
    result["entropy_score"] = entropy

    if entropy > 3.3:
        result["high_entropy"] = True

    # subdomain abuse
    if subdomain and subdomain.count('.') >= 2:
        result["too_many_subdomains"] = True

    # structural deception
    structural_flags = structural_domain_analysis(domain)
    result.update(structural_flags)

    return result


# ---------- Main function ----------
def scan_message_for_urls(text):
    urls = extract_urls(text)

    if not urls:
        return False, []

    findings = []

    for url in urls:
        analysis = analyze_url(url)
        findings.append({"url": url, "analysis": analysis})

    risk = any(
        any(v is True for v in item["analysis"].values())
        for item in findings
    )

    return risk, findings