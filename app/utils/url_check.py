import re
from urllib.parse import urlparse

def analyze_url(url_text):
    """
    Analyze URL for phishing indicators using rule-based detection.
    Returns: dict with label, risk, score
    """
    
    url_text = url_text.strip()
    
    if not url_text:
        return {
            "label": "INVALID",
            "risk": "UNKNOWN",
            "score": 0,
            "details": "Empty URL provided"
        }
    
    # Add protocol if missing
    if not url_text.startswith(('http://', 'https://')):
        url_text = 'https://' + url_text
    
    try:
        parsed = urlparse(url_text)
    except:
        return {
            "label": "INVALID",
            "risk": "UNKNOWN", 
            "score": 0,
            "details": "Invalid URL format"
        }
    
    risk_score = 0
    threats = []
    
    # ========== THREAT ANALYSIS ==========
    
    # 1. Check for IP-based URLs (High Risk)
    if is_ip_address(parsed.netloc):
        risk_score += 35
        threats.append("IP-based URL detected")
    
    # 2. Check for HTTPS vs HTTP
    if parsed.scheme == 'http':
        risk_score += 20
        threats.append("Unencrypted HTTP protocol")
    
    # 3. Check for suspicious TLD or domain patterns
    domain = parsed.netloc.lower().replace('www.', '')
    
    if is_suspicious_domain(domain):
        risk_score += 25
        threats.append("Suspicious domain pattern detected")
    
    # 4. Check for shortened URLs (potential redirect)
    if is_shortened_url(domain):
        risk_score += 15
        threats.append("Shortened URL (potential redirect)")
    
    # 5. Check for suspicious characters in URL
    if has_suspicious_chars(url_text):
        risk_score += 20
        threats.append("Suspicious characters in URL")
    
    # 6. Check for homograph attacks (lookalike domains)
    if has_homograph_chars(domain):
        risk_score += 15
        threats.append("Potential homograph attack")
    
    # 7. Check for too many subdomains
    if len(domain.split('.')) > 4:
        risk_score += 10
        threats.append("Excessive subdomains")
    
    # 8. Check for suspicious keywords in domain
    if has_phishing_keywords(domain + parsed.path):
        risk_score += 20
        threats.append("Phishing keywords detected")
    
    # Cap score at 100
    risk_score = min(risk_score, 100)
    
    # ========== CLASSIFICATION ==========
    
    if risk_score <= 20:
        label = "SAFE"
        risk = "LOW"
    elif risk_score <= 50:
        label = "SUSPICIOUS"
        risk = "MEDIUM"
    else:
        label = "MALICIOUS"
        risk = "HIGH"
    
    return {
        "label": label,
        "risk": risk,
        "score": risk_score,
        "threats": threats,
        "url": url_text
    }


def is_ip_address(netloc):
    """Check if netloc is an IP address"""
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}(:\d+)?$'
    return bool(re.match(ip_pattern, netloc.split(':')[0]))


def is_suspicious_domain(domain):
    """Check for suspicious domain patterns"""
    suspicious_patterns = [
        r'admin',
        r'login',
        r'verify',
        r'confirm',
        r'update',
        r'security',
        r'account',
        r'password',
        r'bank',
        r'paypal',
        r'amazon',
        r'apple',
        r'google',
    ]
    
    # If the domain contains multiple suspicious keywords, it's suspicious
    keyword_count = sum(1 for pattern in suspicious_patterns if re.search(pattern, domain))
    
    # Also check for numeric-heavy domains (common in phishing)
    numeric_ratio = sum(c.isdigit() for c in domain) / len(domain) if domain else 0
    if numeric_ratio > 0.3:
        return True
    
    return keyword_count >= 2


def is_shortened_url(domain):
    """Detect shortened URL services"""
    shortened_services = [
        'bit.ly', 'tinyurl', 'short.link', 'goo.gl', 
        'ow.ly', 'buff.ly', 'is.gd', 'tiny.cc',
        'url.shortener', 'qr.net'
    ]
    return any(service in domain.lower() for service in shortened_services)


def has_suspicious_chars(url):
    """Check for suspicious characters that might hide true URL"""
    suspicious_patterns = [
        r'@',  # Used in URLs like: http://real-site.com@fake-site.com
        r'%',  # URL encoding anomalies
        r'\\',  # Backslashes
    ]
    return any(re.search(pattern, url) for pattern in suspicious_patterns)


def has_homograph_chars(domain):
    """Check for homograph attacks (visually similar characters)"""
    # Common homograph substitutions
    homograph_map = {
        'а': 'a',  # Cyrillic 'a'
        'е': 'e',  # Cyrillic 'e'
        'о': 'o',  # Cyrillic 'o'
        'р': 'p',  # Cyrillic 'p'
        'с': 'c',  # Cyrillic 'c'
        'х': 'x',  # Cyrillic 'x'
        'у': 'y',  # Cyrillic 'y'
    }
    
    for homograph, ascii_char in homograph_map.items():
        if homograph in domain:
            return True
    
    return False


def has_phishing_keywords(text):
    """Check for common phishing keywords"""
    phishing_keywords = [
        'verify', 'confirm', 'update', 'urgent', 'action',
        'click', 'reset', 'reset-password', 'login',
        'signin', 'validate', 'security', 'alert',
        'suspicious', 'activity', 'unusual', 'unlock'
    ]
    
    text_lower = text.lower()
    keyword_count = sum(1 for keyword in phishing_keywords if keyword in text_lower)
    
    return keyword_count >= 2
