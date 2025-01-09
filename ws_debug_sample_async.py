import socket
import threading
import base64
import hashlib
import json

MAGIC_STRING = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


class DebugTicket:
    def __init__(self, number, playable_amount, redeemable_money):
        self.number = number
        self.playable_amount = playable_amount
        self.redeemable_money = redeemable_money

    def __repr__(self):
        return (f"DebugTicket(number={self.number}, "
                f"playable_amount={self.playable_amount}, "
                f"redeemable_money={self.redeemable_money})")


def generate_accept_key(sec_websocket_key):
    # Concatenate the key with the magic string
    concatenated_string = sec_websocket_key + MAGIC_STRING

    # Create a SHA-1 hash of the concatenated string
    sha1_hash = hashlib.sha1(concatenated_string.encode()).digest()

    # Return the Base64-encoded result of the hash
    return base64.b64encode(sha1_hash).decode('utf-8')


def parse_ticket_data(data):
    # Parse the received JSON string and create a DebugTicket object
    try:
        json_data = json.loads(data)
        ticket = DebugTicket(
            number=json_data['number'],
            playable_amount=json_data['playableAmount'],
            redeemable_money=json_data['redeemableMoney']
        )
        return ticket
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing JSON data: {e}")
        return None


def handle_client(client_socket):
    try:
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

            # Once the handshake is complete, enter message handling
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                decoded_data = data.decode('utf-8')
                print(f"Received message: {decoded_data}")

                # Parse the JSON data and create a DebugTicket object
                ticket = parse_ticket_data(decoded_data)
                if ticket:
                    print(f"Parsed Ticket: {ticket}")
                    response_message = f"Ticket {ticket.number} received with amount {ticket.playable_amount}"
                else:
                    response_message = "Failed to parse ticket data"

                # Send a response back to the STM32
                client_socket.sendall(response_message.encode('utf-8'))

    finally:
        client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '192.168.0.1'
    port = 8080
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Got a connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()
