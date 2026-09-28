#!/usr/bin/env python3
"""
Simple TCP (Transmission Control Protocol) client for CYB333 Midterm, Part 1.

Connects to the echo server, lets the user type messages, prints the
server's responses, and disconnects cleanly when the user types 'quit'.
If the server is not running, the connection error is handled gracefully.

Author: Scott Taylor
"""

import socket

HOST = "127.0.0.1"   # Must match the server's host.
PORT = 65432          # Must match the server's port.


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Set a timeout so a dead or unreachable server does not hang forever.
        client_socket.settimeout(5.0)

        try:
            client_socket.connect((HOST, PORT))
        except ConnectionRefusedError:
            # Raised when the server is not running or not listening on this port.
            print(f"[CLIENT] Could not connect to {HOST}:{PORT}. Is the server running?")
            return
        except socket.timeout:
            print("[CLIENT] Connection attempt timed out.")
            return

        print(f"[CLIENT] Connected to {HOST}:{PORT}. Type a message, or 'quit' to exit.")

        while True:
            message = input("You: ").strip()
            if not message:
                continue   # Ignore empty input and prompt again.

            try:
                client_socket.sendall(message.encode("utf-8"))
                data = client_socket.recv(1024)
            except (ConnectionError, socket.timeout) as err:
                print(f"[CLIENT] Lost connection: {err}")
                break

            if not data:
                print("[CLIENT] Server closed the connection.")
                break

            print(f"Server: {data.decode('utf-8')}")

            if message.lower() == "quit":
                break

    print("[CLIENT] Disconnected cleanly.")


if __name__ == "__main__":
    main()
