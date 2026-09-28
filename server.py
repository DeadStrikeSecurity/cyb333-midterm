#!/usr/bin/env python3
"""
Simple TCP (Transmission Control Protocol) echo server for CYB333 Midterm, Part 1.

Listens on a host and port, accepts one client at a time, receives text
messages, and sends a response back. When the client sends 'quit', the
server closes the session cleanly.

Author: Scott Taylor
"""

import socket

HOST = "127.0.0.1"   # Loopback address (IPv4): accept connections from this machine only.
PORT = 65432          # Non-privileged port (any value above 1023 works).


def main():
    # AF_INET = Address Family, Internet (IPv4). SOCK_STREAM = TCP.
    # The 'with' block guarantees the socket is closed when we exit.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Let the address be reused immediately after the server stops.
        # Without this you often get an "address already in use" error while testing.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_socket.bind((HOST, PORT))   # Attach the socket to the host and port.
            server_socket.listen()             # Begin listening for incoming connections.
            print(f"[SERVER] Listening on {HOST}:{PORT} ...")
        except OSError as err:
            print(f"[SERVER] Could not start server: {err}")
            return

        # accept() blocks until a client connects. It returns a new socket
        # dedicated to that client, plus the client's address (IP, port).
        conn, addr = server_socket.accept()
        with conn:
            print(f"[SERVER] Connected by {addr[0]}:{addr[1]}")
            while True:
                try:
                    data = conn.recv(1024)   # Receive up to 1024 bytes at a time.
                except ConnectionError as err:
                    print(f"[SERVER] Connection error: {err}")
                    break

                if not data:
                    # An empty result means the client closed the connection.
                    print("[SERVER] Client disconnected.")
                    break

                message = data.decode("utf-8").strip()
                print(f"[SERVER] Received: {message}")

                if message.lower() == "quit":
                    conn.sendall(b"Server closing connection. Goodbye.")
                    print("[SERVER] Quit received, closing session.")
                    break

                # Echo the message back with a simple acknowledgement.
                response = f"Server received: {message}"
                conn.sendall(response.encode("utf-8"))

    print("[SERVER] Shut down cleanly.")


if __name__ == "__main__":
    main()
