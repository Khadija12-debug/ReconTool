import argparse
import ActiveReconnaissance.port_scanner
import ActiveReconnaissance.banner_grabber
import ActiveReconnaissance.tech_detector

from PassiveReconnaissance.whois_lookup import whois_lookup
from PassiveReconnaissance.dns_enum import dns_lookup
from PassiveReconnaissance.subdomain_enum import get_subdomains_crtsh

from Report_generator import generate_report


def parse_port_list(port_string):
    """Parses comma-separated string into list of ports"""
    try:
        return [int(p.strip()) for p in port_string.split(",")]
    except ValueError:
        print("[-] Invalid port list format. Use comma-separated values like 80,443,22")
        return []


def main():
    print("=== Active Reconnaissance ===")
    target_ip = input("Enter target IP or domain for active recon: ").strip()

    print("\n=== Passive Reconnaissance ===")
    target_domain = input("Enter domain for passive recon: ").strip()

    print("\n=== Optional CLI-Based Active Recon (Advanced) ===")

    parser = argparse.ArgumentParser(description="Optional CLI active recon")
    parser.add_argument("--scan-ports", action="store_true", help="Perform port scanning")
    parser.add_argument("--grab-banners", action="store_true", help="Perform banner grabbing")
    parser.add_argument("--detect-tech", action="store_true", help="Detect website technologies")
    parser.add_argument("--ports", help="Comma-separated ports for banner grabbing")

    args = parser.parse_args()
    open_ports = []

    # Step 1: Port Scanning (optional)
    if args.scan_ports:
        open_ports = ActiveReconnaissance.port_scanner.run_port_scan(target_ip)

    # Step 2: Banner Grabbing (optional)
    if args.grab_banners:
        if args.ports:
            ports = parse_port_list(args.ports)
        elif open_ports:
            ports = open_ports
        else:
            print("[-] No ports specified or scanned. Use --ports or enable --scan-ports first.")
            return
        ActiveReconnaissance.banner_grabber.run_banner_grab(target_ip, ports)

    # Step 3: Technology Detection (optional)
    if args.detect_tech:
        url = target_ip
        if not url.startswith("http"):
            url = "http://" + url
        ActiveReconnaissance.tech_detector.detect_technologies(url)

    # FINAL STEP: Generate Report
    print("\n[+] Generating final recon report...")
    generate_report(target_ip, target_domain)


if __name__ == "__main__":
    main()
