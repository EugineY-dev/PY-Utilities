import socket

# Define server details
server_ip = "192.168.0.101"  # Replace with your Flex-Port IP
# server_port = 8080         # Replace with your desired port
server_port = 61630         # Replace with your desired port

# Create socket connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Example to send and receive data
client_socket.sendall(b'Hello Flex-Port')
response = client_socket.recv(1024)
print(f"Received: {response}")

client_socket.close()
