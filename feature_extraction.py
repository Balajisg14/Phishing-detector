import re

def extract_features(url):
    # Safety check
    if not isinstance(url, str):
        url = ""

    features = []

    # 1. URL length
    features.append(len(url))

    # 2. Number of dots
    features.append(url.count('.'))

    # 3. Number of hyphens
    features.append(url.count('-'))

    # 4. Number of @ symbols
    features.append(url.count('@'))

    # 5. Number of digits
    features.append(sum(char.isdigit() for char in url))

    # 6. Number of special characters
    features.append(len(re.findall(r'[?=&%]', url)))

    # 7. HTTPS present
    features.append(1 if url.startswith("https") else 0)

    # 8. IP address present
    ip_pattern = re.compile(r'(\d{1,3}\.){3}\d{1,3}')
    features.append(1 if ip_pattern.search(url) else 0)

    # 9. URL shortening service
    shortening_services = ['bit.ly', 'tinyurl', 'goo.gl', 't.co']
    features.append(1 if any(service in url for service in shortening_services) else 0)

    # 10. Suspicious words
    suspicious_words = ['login', 'verify', 'update', 'secure', 'account', 'bank']
    features.append(1 if any(word in url.lower() for word in suspicious_words) else 0)

    # 🔥 THIS LINE IS CRITICAL
    return features
