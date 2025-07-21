import dns.resolver

def dns_lookup(domain):
    records = {}
    for rtype in ["A", "MX", "TXT", "NS"]:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            records[rtype] = [r.to_text() for r in answers]
        except Exception as e:
            records[rtype] = [f"Error: {e}"]
    return records
