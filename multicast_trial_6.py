import socket
import os
import platform
import re

def get_ethernet_ip():
    """Detects an Ethernet IP address on Windows using only the standard library."""
    interfaces = []
    if platform.system() == "Windows":
        # Use 'ipconfig' to get network details
        result = os.popen("ipconfig").read()
        # Look for Ethernet interfaces (e.g., "Ethernet adapter Ethernet" or similar)
        for block in result.split("\n\n"):
            if re.search(r"Ethernet adapter Ethernet(\s*\d*):", block):
                for line in block.splitlines():
                    if "IPv4 Address" in line or "IPv4 Address." in line:  # Handle possible "IPv4 Address" variations
                        ip = line.split(":")[-1].strip()
                        return ip
    else:
        # Unix-like (Linux/Mac) systems can use 'ifconfig' for Ethernet detection
        result = os.popen("ifconfig").read()
        for block in result.split("\n\n"):
            if "eth" in block or "en" in block:  # Typical Ethernet naming conventions
                lines = block.splitlines()
                for line in lines:
                    if "inet " in line:
                        ip = line.split()[1]
                        return ip
    return None


def send_multicast_message(ip_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(ip_address))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    message = b"5ecReTPaS5W0rD"
    sock.sendto(message, ("239.0.0.10", 5010))
    print("Multicast message sent.")
    sock.close()


def receive_multicast_message(ip_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind(("", 5011))

    group = socket.inet_aton("239.0.0.10")
    mreq = struct.pack("4s4s", group, socket.inet_aton(ip_address))
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
local_ip = get_ethernet_ip()
if local_ip:
    print(f"Using local IP: {local_ip}")
    send_multicast_message(local_ip)
    receive_multicast_message(local_ip)
else:
    print("No Ethernet interface found. Please ensure an Ethernet connection is available.")
