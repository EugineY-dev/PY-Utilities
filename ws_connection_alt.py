import socket


def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Specify the IP address and port
    # host = '192.168.0.1'
    host = '192.168.0.101'
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

        # Receive the data in small chunks and retransmit it
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received message: {data.decode('utf-8')}")
            client_socket.sendall(data)  # Echo back the received message

        # Close the connection
        client_socket.close()


if __name__ == "__main__":
    start_server()
