#!/usr/bin/env python3
"""
Simple TCP (Transmission Control Protocol) port scanner for CYB333 Midterm, Part 2.

Scans a range of ports on an authorized target and reports which ones are
open. A short delay is added between ports to keep the scan polite and to
respect rate-limiting guidance.

AUTHORIZED TARGETS ONLY:
    - localhost / 127.0.0.1  (your own machine)
    - scanme.nmap.org        (a host the Nmap project provides for scan testing)
Scanning any other system without explicit written permission is illegal and
against this assignment's rules.

Usage examples:
    python3 port_scanner.py 127.0.0.1
    python3 port_scanner.py 127.0.0.1 --start 1 --end 1024
    python3 port_scanner.py 127.0.0.1 --common
    python3 port_scanner.py scanme.nmap.org --ports 21,22,80,443

Author: Scott Taylor
"""

import argparse
import socket
import sys
import time
from datetime import datetime

# Map well-known ports to service names, used only to label the results.
COMMON_SERVICES = {
    21: "FTP (File Transfer Protocol)",
    22: "SSH (Secure Shell)",
    23: "Telnet",
    25: "SMTP (Simple Mail Transfer Protocol)",
    53: "DNS (Domain Name System)",
    80: "HTTP (HyperText Transfer Protocol)",
    110: "POP3 (Post Office Protocol version 3)",
    143: "IMAP (Internet Message Access Protocol)",
    443: "HTTPS (HTTP Secure)",
    3306: "MySQL database",
    3389: "RDP (Remote Desktop Protocol)",
    8080: "HTTP alternate",
}

# Targets this scanner is allowed to hit, per the assignment rules.
AUTHORIZED = {"127.0.0.1", "localhost", "scanme.nmap.org"}


def resolve_host(target):
    """Resolve a hostname to an IPv4 address, or exit with a clear message."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[ERROR] Could not resolve host '{target}'. Check the name and your connection.")
        sys.exit(1)


def scan_port(ip, port, timeout):
    """
    Return True if the TCP port is open, False otherwise.

    connect_ex() returns 0 on success instead of raising an exception, which
    makes it convenient for scanning many ports inside a loop.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            return sock.connect_ex((ip, port)) == 0
        except socket.error:
            return False


def build_port_list(args):
    """Turn the command-line options into a validated list of ports."""
    if args.common:
        return sorted(COMMON_SERVICES.keys())

    if args.ports:
        ports = []
        for chunk in args.ports.split(","):
            chunk = chunk.strip()
            if not chunk.isdigit():
                print(f"[ERROR] '{chunk}' is not a valid port number.")
                sys.exit(1)
            ports.append(int(chunk))
    else:
        if args.start > args.end:
            print("[ERROR] --start cannot be greater than --end.")
            sys.exit(1)
        ports = list(range(args.start, args.end + 1))

    # Validate every port: TCP ports run from 1 to 65535.
    for p in ports:
        if p < 1 or p > 65535:
            print(f"[ERROR] Port {p} is out of range. Valid ports are 1 to 65535.")
            sys.exit(1)
    return ports


def main():
    parser = argparse.ArgumentParser(description="Simple, polite TCP port scanner.")
    parser.add_argument("target", help="Authorized target: localhost, 127.0.0.1, or scanme.nmap.org")
    parser.add_argument("--start", type=int, default=1, help="First port in a range (default 1)")
    parser.add_argument("--end", type=int, default=1024, help="Last port in a range (default 1024)")
    parser.add_argument("--ports", help="Comma-separated ports, for example 21,22,80,443")
    parser.add_argument("--common", action="store_true", help="Scan a built-in list of common ports")
    parser.add_argument("--timeout", type=float, default=1.0, help="Per-port timeout in seconds (default 1.0)")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between ports in seconds (default 0.1)")
    args = parser.parse_args()

    # Ethical guardrail: warn and require confirmation for any non-approved target.
    if args.target not in AUTHORIZED:
        print(f"[WARNING] '{args.target}' is not on the authorized list "
              f"({', '.join(sorted(AUTHORIZED))}).")
        print("[WARNING] Only scan systems you own or have explicit written permission to test.")
        confirm = input("Type 'yes' to confirm you are authorized to scan this target: ").strip().lower()
        if confirm != "yes":
            print("[ABORTED] Scan cancelled.")
            sys.exit(0)

    ip = resolve_host(args.target)
    ports = build_port_list(args)

    print(f"\n[INFO] Scanning {args.target} ({ip})")
    print(f"[INFO] {len(ports)} port(s), timeout {args.timeout}s, delay {args.delay}s between ports")
    print(f"[INFO] Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    open_ports = []
    start_time = time.time()

    try:
        for index, port in enumerate(ports, start=1):
            # Progress indicator that overwrites the same terminal line.
            print(f"\r[SCAN] Checking port {port} ({index}/{len(ports)}) ...", end="", flush=True)
            if scan_port(ip, port, args.timeout):
                service = COMMON_SERVICES.get(port, "unknown service")
                open_ports.append((port, service))
            time.sleep(args.delay)   # Politeness delay to avoid hammering the target.
    except KeyboardInterrupt:
        print("\n[INFO] Scan interrupted by user (Ctrl+C).")

    elapsed = time.time() - start_time
    print("\n")   # Move past the progress line.

    if open_ports:
        print("[RESULTS] Open ports:")
        for port, service in open_ports:
            print(f"    {port:>5}/tcp  open   {service}")
    else:
        print("[RESULTS] No open ports found in the scanned set.")

    print(f"\n[INFO] Finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[INFO] Scanned {len(ports)} port(s) in {elapsed:.2f} seconds.")


if __name__ == "__main__":
    main()
