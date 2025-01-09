import socket
import struct
import time

# Multicast group and ports as per your requirements
MULTICAST_GROUP = '239.0.0.10'
MULTICAST_PORT_SEND = 5010
MULTICAST_PORT_RECEIVE = 5011

def send_multicast_message():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # Set the time-to-live for messages to 1 for local network use
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

    message = b'Hello, is FlexPay Kiosk available?'

    try:
        # Send the multicast message to the group
        print(f"Sending message to multicast group {MULTICAST_GROUP}:{MULTICAST_PORT_SEND}")
        sock.sendto(message, (MULTICAST_GROUP, MULTICAST_PORT_SEND))
        print("Message sent.")
    finally:
        sock.close()

def receive_response():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Allow multiple sockets to use the same port (necessary for multicast)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to the server address and port to listen for responses
    sock.bind(('', MULTICAST_PORT_RECEIVE))

    # Tell the operating system to add the socket to the multicast group on the specified interface
    group = socket.inet_aton(MULTICAST_GROUP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Set a timeout so the socket does not block indefinitely when trying to receive data
    sock.settimeout(5)

    try:
        print("Waiting to receive response...")
        while True:
            try:
                data, address = sock.recvfrom(1024)
                print(f"Received response from {address}: {data.decode()}")
                break
            except socket.timeout:
                print("No response received, retrying...")
                break
    finally:
        sock.close()

# Run both functions
send_multicast_message()
time.sleep(1)  # Short delay to allow the message to propagate
receive_response()
