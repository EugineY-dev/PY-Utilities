import socket
import struct

# Multicast configuration parameters
MCAST_GRP = "239.0.0.10"  # Multicast group for communication
MCAST_PORT_SEND = 5010  # Port for sending messages
MCAST_PORT_RECV = 5011  # Port to receive responses
MCAST_IF_IP = "192.168.0.100"  # IP address of your network interface (update as needed)


def send_multicast_message():
    """Function to send a multicast message."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Specify the network interface to use for sending the multicast
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(MCAST_IF_IP))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)  # Set TTL for multicast packets

    # Message to be sent
    message = b"Hello, Flexpay Kiosk"
    # message = b"5ecReTPaS5W0rD"
    sock.sendto(message, (MCAST_GRP, MCAST_PORT_SEND))
    print("Multicast message sent.")
    sock.close()


def receive_multicast_message():
    """Function to listen for and receive responses."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind(("", MCAST_PORT_RECV))  # Bind to the specified receive port

    # Join the multicast group to listen for responses
    group = socket.inet_aton(MCAST_GRP)
    mreq = struct.pack("4s4s", group, socket.inet_aton(MCAST_IF_IP))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print("Waiting for a response from the Flexpay Kiosk...")
    try:
        while True:
            data, address = sock.recvfrom(1024)  # Adjust buffer size if needed
            print(f"Received message: {data} from {address}")
            break  # Break after receiving a response (can be adjusted based on needs)
    except KeyboardInterrupt:
        print("Stopped listening.")
    finally:
        sock.close()


# Execute the functions to send and receive messages
send_multicast_message()
receive_multicast_message()
