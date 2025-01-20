import socket
import base64
import hashlib

# WebSocket handshake constants
# websocket_url = "192.168.0.101"  # Replace with your server's IP
websocket_url = "192.168.0.100"  # Replace with your server's IP
port = 61630
path = "/ws/flexpay/client/v1/communication"
key = base64.b64encode(b'websocket-key').decode('utf-8')  # Random unique key for handshake

# Create a WebSocket client using raw sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((websocket_url, port))

# Send WebSocket handshake request
handshake_request = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {websocket_url}:{port}\r\n"
    f"Upgrade: websocket\r\n"
    f"Connection: Upgrade\r\n"
    f"Sec-WebSocket-Key: {key}\r\n"
    f"Sec-WebSocket-Version: 13\r\n"
    f"\r\n"
)
sock.send(handshake_request.encode('utf-8'))

# Receive the server's response
response = sock.recv(1024)
print("Handshake response:\n", response.decode())

# NOTE: You'd need to manually handle WebSocket frame encoding/decoding here
# This includes framing your messages according to the WebSocket protocol,
# which requires careful attention to control bits, payload length, masking, etc.

# Example data to send (must be framed correctly, this part is simplified and illustrative)
message = b"Hello WebSocket Server"  # Example payload

# Closing the socket (ensure you implement a proper close handshake in real use)
sock.close()
