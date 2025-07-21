import whois

def whois_lookup(domain):
    try:
        result = whois.whois(domain)
        return result
    except Exception as e:
        return f"Error: {e}"