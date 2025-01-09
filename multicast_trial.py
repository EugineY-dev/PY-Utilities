import socket
import struct
import time

# Multicast configuration
MULTICAST_GROUP = '239.0.0.10'  # Multicast IP address
MULTICAST_PORT = 5010  # Port to send/receive on
RECEIVE_PORT = 5011  # Expected response port


def multicast_sender():
    # Set up the socket for sending
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    # Message to send
    # message = b"Hello, is the FlexPay Kiosk here?"
    message = b""

    try:
        # Send the message to the multicast group
        print(f"Sending multicast message to {MULTICAST_GROUP}:{MULTICAST_PORT}")
        sock.sendto(message, (MULTICAST_GROUP, MULTICAST_PORT))
        print("Message sent.")
    finally:
        sock.close()


def multicast_receiver():
    # Set up the socket for receiving
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind(('', RECEIVE_PORT))

    # Join the multicast group
    mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Listening for responses on port {RECEIVE_PORT}...")
    try:
        # Receive messages
        while True:
            data, address = sock.recvfrom(1024)
            print(f"Received response from {address}: {data.decode()}")
    except KeyboardInterrupt:
        print("\nExiting.")
    finally:
        sock.close()


# Run sender and receiver as a quick test
if __name__ == "__main__":
    multicast_sender()
    time.sleep(1)  # Give some time for the receiver to catch the response
    multicast_receiver()
