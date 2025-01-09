import json
import socket
import time

# Create the request message
request_message = {
    "timestamp": int(time.time() * 1000),  # Example: Use current timestamp in milliseconds
    "version": 1,
    "token": "4fccbefb-9011-482b-8a20-fc610ba207e3",  # Example token; replace as needed
    "data": {
        "messageType": "CHECK_TICKET_EXISTENCE",
        "ticketNumber": "172182202022221610"  # Example ticket number; replace as needed
    }
}

# Serialize to JSON string
request_message_json = json.dumps(request_message)

# Configure the socket connection
server_ip = "192.168.0.101"  # Replace with Flex-Port server's IP
server_port = 61630  # Replace with the correct port

# Establish and send data over socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((server_ip, server_port))
    sock.sendall(request_message_json.encode('utf-8'))

    # Receive the response (assuming a response is returned)
    response_data = sock.recv(4096)
    response_message = json.loads(response_data.decode('utf-8'))

# Output the response
print("Received Response:", json.dumps(response_message, indent=4))
