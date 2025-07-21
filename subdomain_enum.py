import requests

def get_subdomains_crtsh(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return [f"Error: Failed to fetch data. Status code: {res.status_code}"]
        data = res.json()
        subdomains = set()
        for entry in data:
            name = entry.get("name_value", "")
            for sub in name.split("\n"):
                if sub.endswith(domain):
                    subdomains.add(sub.strip())
        return list(subdomains)
    except Exception as e:
        return [f"Error: {e}"]
