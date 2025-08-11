import socket
import struct
import argparse
import sys

class TCPClient:
    def __init__(self, host: str, port: int, timeout: float = 5.0):
        """
        host: server IP or hostname
        port: server port
        timeout: socket timeout in seconds
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None

    def connect(self):
        """Create and connect the socket."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))

    def send_floats(self, a: float, b: float):
        """
        Pack two floats into 8 bytes (4 each, little-endian) and send.
        """
        if self.sock is None:
            raise RuntimeError("Socket is not connected")
        data = f"VEL,{a:.3f},{b:.3f}\n"
        self.sock.sendall(data.encode('ascii'))

    def receive(self, bufsize: int = 1024):
        """Receive up to bufsize bytes from the server."""
        if self.sock is None:
            raise RuntimeError("Socket is not connected")
        return self.sock.recv(64).decode('ascii', errors='ignore').strip()

    def close(self):
        """Cleanly close the socket."""
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.sock.close()
            self.sock = None

# def main():
    # parser = argparse.ArgumentParser(description="Send two floats via TCP")
    # parser.add_argument("host", help="Server IP or hostname")
    # parser.add_argument("port", type=int, help="Server port")
    # parser.add_argument("a", type=float, help="First float value")
    # parser.add_argument("b", type=float, help="Second float value")
    # args = parser.parse_args()

    # client = TCPClient(host = 'x.x.x.x', port=xxxx, timeout= 5.0)
    # try:
    #     print(f"Connecting to {client.host}:{client.port}...")
    #     client.connect()
    #     while(True):
    #         line = input("Enter velocities (fwd, turn): ").strip()
    #         if not line or line.lower() in ('q', 'quit', 'exit'):
    #             print("Closing connection.")
    #             break

    #         # Expecting two floats separated by space or comma
    #         parts = line.replace(',', ' ').split()
    #         if len(parts) != 2:
    #             print("please enter exactly two numbers, e.g. 1.0 -0.5")
    #             continue

    #         try:
    #             fwd = float(parts[0])
    #             turn = float(parts[1])
    #         except ValueError:
    #             print("invalid numbers, try again")
    #             continue
            
    #         client.send_floats(fwd, turn)
    #         # Optionally read response:
    #         resp = client.receive()
    #         if resp:
    #             print("Received:", resp)
    # except Exception as e:
    #     print("Error:", e, file=sys.stderr)
    # finally:
    #     client.close()
    #     print("Connection closed.")

if __name__ == "__main__":
    pass
    # main()
