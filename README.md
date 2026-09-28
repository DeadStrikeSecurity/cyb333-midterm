# CYB333 Midterm: Network Programming in Python

Scott Taylor, CYB333 Security Automation

This repository contains two Python programs written for the CYB333 midterm:
a basic client-server socket application and a TCP (Transmission Control
Protocol) port scanner.

## Contents

| File | Description |
|------|-------------|
| `server.py` | TCP echo server that listens for a connection and responds to messages. |
| `client.py` | TCP client that connects to the server, sends messages, and prints replies. |
| `port_scanner.py` | Scans a range of ports on an authorized target and reports open ports. |

## Requirements

Python 3.8 or newer. All scripts use only the Python standard library, so no
extra packages are needed.

## Part 1: Socket connection

Open two terminals.

Terminal 1 (start the server first):

```bash
python3 server.py
```

Terminal 2 (start the client):

```bash
python3 client.py
```

Type a message in the client and press Enter to see the server's response.
Type `quit` to close the session cleanly. If you start the client while the
server is not running, the client reports the connection error instead of
crashing.

## Part 2: Port scanner

**Authorized targets only:** `localhost` / `127.0.0.1` and `scanme.nmap.org`.
Scanning any other system without explicit written permission is illegal.

```bash
# Scan a built-in list of common ports on your own machine
python3 port_scanner.py 127.0.0.1 --common

# Scan a custom range on localhost
python3 port_scanner.py 127.0.0.1 --start 1 --end 1024

# Scan selected ports on the Nmap test host
python3 port_scanner.py scanme.nmap.org --ports 21,22,80,443
```

Options:

- `--start` / `--end`: first and last port in a range (default 1 to 1024).
- `--ports`: comma-separated list, for example `21,22,80,443`.
- `--common`: scan a built-in set of well-known ports.
- `--timeout`: per-port timeout in seconds (default 1.0).
- `--delay`: delay between ports in seconds (default 0.1), used for polite,
  rate-limited scanning.

The scanner validates port numbers, resolves and checks the host, adds a delay
between ports, shows a progress indicator, and prints timestamps at the start
and end so results can be verified.
