import socket
import base64
import hashlib
import struct

# Constants
MULTICAST_GROUP = '239.0.0.10'
MULTICAST_PORT = 5010
RESPONSE_PORT = 5011


def discover_flexpay_kiosk():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Windows-specific fix
    mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    sock.bind(('', RESPONSE_PORT))

    # Send multicast message
    message = b"FLEXPAY_DISCOVERY"
    sock.sendto(message, (MULTICAST_GROUP, MULTICAST_PORT))

    # Listen for response
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received response from {addr}: {data.decode()}")
        return data.decode().strip()


def connect_to_websocket_server(address):
    # Establish a socket connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((address, 61630))

    # Perform WebSocket handshake
    websocket_key = base64.b64encode(hashlib.sha1(b"websocket_key").digest()).decode()
    request = f"GET /ws/flexpay/client/v1/communication HTTP/1.1\r\n" \
              f"Host: {address}\r\n" \
              "Upgrade: websocket\r\n" \
              "Connection: Upgrade\r\n" \
              f"Sec-WebSocket-Key: {websocket_key}\r\n" \
              "Sec-WebSocket-Version: 13\r\n\r\n"
    sock.send(request.encode())

    # Receive and print server response
    response = sock.recv(4096)
    print(f"Handshake response:\n{response.decode()}")

    # Send a message
    message = "Hello from Python!"
    sock.send(message.encode())

    # Receive a response
    response = sock.recv(4096)
    print(f"Received: {response.decode()}")

    # Close the connection
    sock.close()


if __name__ == "__main__":
    domain_name = discover_flexpay_kiosk()
    connect_to_websocket_server(domain_name)
