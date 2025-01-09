import socket
import base64
import hashlib

MAGIC_STRING = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def generate_accept_key(sec_websocket_key):
    # Concatenate the key with the magic string
    concatenated_string = sec_websocket_key + MAGIC_STRING

    # Create a SHA-1 hash of the concatenated string
    sha1_hash = hashlib.sha1(concatenated_string.encode()).digest()

    # Return the Base64-encoded result of the hash
    return base64.b64encode(sha1_hash).decode('utf-8')


def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Specify the IP address and port
    host = '192.168.0.1'
    port = 8080

    # Bind the socket to the IP address and port
    server_socket.bind((host, port))

    # Start listening for incoming connections
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        # Establish a connection
        client_socket, addr = server_socket.accept()
        print(f"Got a connection from {addr}")

        # Receive the client's handshake request
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Handshake request: {request}")

        # Find the Sec-WebSocket-Key in the client's request
        sec_websocket_key = None
        for line in request.splitlines():
            if "Sec-WebSocket-Key" in line:
                sec_websocket_key = line.split(": ")[1]
                break

        # Generate the Sec-WebSocket-Accept value using the key
        if sec_websocket_key:
            accept_key = generate_accept_key(sec_websocket_key)

            # Construct the response
            response = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
            )

            # Send the handshake response
            client_socket.send(response.encode('utf-8'))
            print(f"Handshake response sent with Sec-WebSocket-Accept: {accept_key}")

            # Simple echo after the handshake
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received message: {data.decode('utf-8')}")
                # client_socket.sendall(data)  # Echo back the received message
                client_socket.sendall(b"Hello from PC!")  # Echo back the received message

        # Close the connection
        client_socket.close()


if __name__ == "__main__":
    start_server()

# import socket
#
#
# def start_server():
#     # Create a socket object
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#     # Specify the IP address and port
#     host = '192.168.0.1'
#     port = 8080
#
#     # Bind the socket to the IP address and port
#     server_socket.bind((host, port))
#
#     # Start listening for incoming connections
#     server_socket.listen(5)
#     print(f"Server listening on {host}:{port}")
#
#     while True:
#         # Establish a connection
#         client_socket, addr = server_socket.accept()
#         print(f"Got a connection from {addr}")
#
#         # Receive the client's handshake request
#         request = client_socket.recv(1024).decode('utf-8')
#         print(f"Handshake request: {request}")
#
#         # Manually send a basic WebSocket handshake response (without real processing)
#         response = (
#             "HTTP/1.1 101 Switching Protocols\r\n"
#             "Upgrade: websocket\r\n"
#             "Connection: Upgrade\r\n"
#             "Sec-WebSocket-Accept: fake_websocket_accept_value\r\n\r\n"
#         )
#
#         # Send the response
#         client_socket.send(response.encode('utf-8'))
#         print("Handshake response sent")
#
#         # Simple echo after the handshake
#         while True:
#             data = client_socket.recv(1024)
#             if not data:
#                 break
#             print(f"Received message: {data.decode('utf-8')}")
#             client_socket.sendall(data)  # Echo back the received message
#
#         # Close the connection
#         client_socket.close()
#
# if __name__ == "__main__":
#     start_server()
