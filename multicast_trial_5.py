import socket
import struct

# Multicast parameters
MCAST_GRP = "239.0.0.10"  # Multicast group
MCAST_PORT_SEND = 5010  # Port for sending to the kiosk
MCAST_PORT_RECV = 5011  # Port to receive responses from the kiosk


def get_active_interface_ip():
    """Find the active IP address of the device."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            # Connect to a public address to determine local IP
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except Exception as e:
            print(f"Error obtaining active interface IP: {e}")
            return "127.0.0.1"  # Fallback IP (localhost)


def send_multicast_message():
    MCAST_IF_IP = get_active_interface_ip()  # Automatically detect active IP
    print(f"Using local IP: {MCAST_IF_IP}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # Specify interface for multicast using the detected IP
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(MCAST_IF_IP))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    message = b"5ecReTPaS5W0rD"
    sock.sendto(message, (MCAST_GRP, MCAST_PORT_SEND))
    print("Multicast message sent.")
    sock.close()


def receive_multicast_message():
    MCAST_IF_IP = get_active_interface_ip()  # Automatically detect active IP
    print(f"Using local IP: {MCAST_IF_IP} for receiving")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind(("", MCAST_PORT_RECV))

    group = socket.inet_aton(MCAST_GRP)
    mreq = struct.pack("4s4s", group, socket.inet_aton(MCAST_IF_IP))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print("Waiting for a response from the Flexpay Kiosk...")
    while True:
        try:
            data, address = sock.recvfrom(1024)
            print(f"Received message: {data} from {address}")
            break
        except KeyboardInterrupt:
            print("Stopped listening.")
            break
    sock.close()

# Run the functions

send_multicast_message()
receive_multicast_message()
