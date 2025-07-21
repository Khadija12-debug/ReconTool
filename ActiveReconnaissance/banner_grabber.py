# active/banner_grabber.py

import socket

def grab_banner(target, port, timeout=2):
    """
    Connects to the target on the specified port and attempts to grab the banner.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((target, port))
            try:
                banner = s.recv(1024).decode().strip()
                if banner:
                    return f"[+] {target}:{port} - {banner}"
                else:
                    return f"[+] {target}:{port} - No banner received"
            except socket.timeout:
                return f"[-] {target}:{port} - Timeout while grabbing banner"
    except Exception as e:
        return f"[-] {target}:{port} - {str(e)}"

def run_banner_grab(target, ports):
    """
    Grabs banners from a list of ports on the target.
    """
    print(f"\n[+] Starting banner grabbing on {target}...\n")
    for port in ports:
        result = grab_banner(target, port)
        print(result)
