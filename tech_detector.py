# active/tech_detector.py

import requests
from bs4 import BeautifulSoup

def detect_technologies(url):
    """
    Detects basic technologies used by analyzing HTTP headers and HTML content.
    """
    print(f"\n[+] Starting technology detection for {url}...\n")

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"[-] Error fetching URL: {e}")
        return

    headers = response.headers
    techs = []

    # Server info
    server = headers.get('Server')
    if server:
        techs.append(f"Server: {server}")

    # X-Powered-By header (e.g., PHP, ASP.NET)
    x_powered = headers.get('X-Powered-By')
    if x_powered:
        techs.append(f"X-Powered-By: {x_powered}")

    # Check for CMS or frameworks in HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    generator = soup.find('meta', attrs={"name": "generator"})
    if generator and generator.get("content"):
        techs.append(f"Generator: {generator['content']}")

    # Check for JS libraries and frameworks
    scripts = soup.find_all('script', src=True)
    for script in scripts:
        src = script['src']
        if "jquery" in src:
            techs.append("Library: jQuery")
        if "wp-content" in src or "wordpress" in src:
            techs.append("CMS: WordPress")
        if "bootstrap" in src:
            techs.append("Framework: Bootstrap")

    if techs:
        print("[+] Technologies Detected:")
        for tech in set(techs):
            print("  -", tech)
    else:
        print("[-] No obvious technologies detected.")
