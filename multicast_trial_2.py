import socket
import struct
import time

MULTICAST_GROUP = '239.0.0.10'
MULTICAST_PORT = 5010

# Setup socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ttl = struct.pack('b', 1)  # Set TTL for local network
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

# Send a test message every few seconds
try:
    while True:
        message = b'Test message from Flex-port client'
        print(f"Sending message: {message}")
        sock.sendto(message, (MULTICAST_GROUP, MULTICAST_PORT))
        time.sleep(5)
except KeyboardInterrupt:
    print("Exiting multicast test.")
finally:
    sock.close()
