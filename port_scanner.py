# active/port_scanner.py

import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(target, port, timeout=1):
    """Scan a single port on the target"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            if result == 0:
                return port
    except Exception:
        pass
    return None

def run_port_scan(target, ports=None, max_threads=100):
    """
    Scan a list of ports on the target.
    If no port list is given, it scans common ports.
    """
    if ports is None:
        ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389, 8080]

    print(f"\n[+] Starting port scan on {target}...\n")

    open_ports = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(lambda port: scan_port(target, port), ports)

    for port, result in zip(ports, results):
        if result:
            print(f"[+] Port {port} is OPEN")
            open_ports.append(port)

    if not open_ports:
        print("[-] No open ports found.")
    return open_ports
