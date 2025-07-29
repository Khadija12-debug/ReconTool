from datetime import datetime

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ActiveReconnaissance.port_scanner import run_port_scan
from ActiveReconnaissance.banner_grabber import grab_banner
from ActiveReconnaissance.tech_detector import detect_technologies

from PassiveReconnaissance.whois_lookup import whois_lookup
from PassiveReconnaissance.dns_enum import dns_lookup
from PassiveReconnaissance.subdomain_enum import get_subdomains_crtsh


def generate_report(target_ip, target_domain, output_dir="reports"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/recon_report_{target_domain or target_ip}_{timestamp}.txt"

    os.makedirs(output_dir, exist_ok=True)

    with open(filename, "w") as report:
        report.write(f"Reconnaissance Report - {datetime.now()}\n")
        report.write("=" * 60 + "\n")

        if target_domain:
            # Passive Recon
            report.write("\n[PASSIVE RECONNAISSANCE]\n")
            report.write("-" * 60 + "\n")

            # WHOIS
            report.write("\n[+] WHOIS Information:\n")
            whois_data = whois_lookup(target_domain)
            report.write(str(whois_data) + "\n")

            # DNS Records
            report.write("\n[+] DNS Records:\n")
            dns_records = dns_lookup(target_domain)
            for rtype, values in dns_records.items():
                report.write(f"  {rtype}: {', '.join(values)}\n")

            # Subdomains
            report.write("\n[+] Subdomains from crt.sh:\n")
            subdomains = get_subdomains_crtsh(target_domain)
            for sub in subdomains:
                report.write(f"  - {sub}\n")

        if target_ip:
            # Active Recon
            report.write("\n[ACTIVE RECONNAISSANCE]\n")
            report.write("-" * 60 + "\n")

            # Port Scan
            report.write("\n[+] Open Ports:\n")
            open_ports = run_port_scan(target_ip)
            for port in open_ports:
                report.write(f"  - {port}\n")

            # Banner Grabbing
            report.write("\n[+] Banners:\n")
            for port in open_ports:
                result =grab_banner(target_ip, port)
                report.write(f"  {result}\n")

            # Technology Detection
            report.write("\n[+] Web Technology Fingerprinting:\n")
            if target_domain:
                detect_technologies(f"http://{target_domain}")  # or https
            else:
                detect_technologies(f"http://{target_ip}")

            if techs:
                for t in techs:
                    report.write(f"  - {t}\n")  
            else:
                report.write("  [-] No obvious technologies detected.\n")

    print(f"\n[+] Report generated: {filename}")
