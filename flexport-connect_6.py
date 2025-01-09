import socket
import base64
import hashlib
import json

# WebSocket configuration
HOST = "192.168.0.101"
PORT = 61630
RESOURCE = "/ws/flexpay/client/v1/communication"


# WebSocket handshake headers
def create_handshake_request():
    key = base64.b64encode(b"random_key").decode("utf-8")
    return (
        f"GET {RESOURCE} HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    )


# Frame WebSocket messages
def frame_websocket_message(message):
    encoded_message = message.encode("utf-8")
    length = len(encoded_message)
    if length <= 125:
        return bytes([0x81, length]) + encoded_message
    elif length <= 65535:
        return bytes([0x81, 126]) + length.to_bytes(2, byteorder="big") + encoded_message
    else:
        raise ValueError("Message too long")


# Unframe WebSocket messages
def unframe_websocket_message(data):
    payload_length = data[1] & 0x7F
    if payload_length == 126:
        mask_start = 4
        payload_start = 8
    elif payload_length == 127:
        mask_start = 10
        payload_start = 14
    else:
        mask_start = 2
        payload_start = 6

    mask = data[mask_start:mask_start + 4]
    encoded_payload = data[payload_start:]
    payload = bytes(b ^ mask[i % 4] for i, b in enumerate(encoded_payload))
    return payload.decode("utf-8")


# Device registration message
def create_register_message():
    return {
        "timestamp": 1721124745135,  # Example timestamp; replace as needed
        "version": 1,
        "token": "c5287677-4b7a-4f31-acd5-5e5ddf023c76",  # Replace with your token
        "data": {
            "messageType": "REGISTER_FLEX_PORT_CLIENT",
            "deviceId": "230E568803000093",  # Replace with your deviceId
            "softwareVersion": "GCOAM-1.14.x.4.3.1.SNAPSHOT"  # Replace with your software version
        }
    }


# Connect and communicate with WebSocket server
def websocket_communication():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Send handshake request
        handshake_request = create_handshake_request()
        s.sendall(handshake_request.encode("utf-8"))

        # Receive handshake response
        response = s.recv(1024).decode("utf-8")

        print(response)

        if "101 Switching Protocols" not in response:
            print("Handshake failed!")
            print(response)
            return

        print("Handshake successful!")

        # Send device registration message
        register_message = create_register_message()
        framed_message = frame_websocket_message(json.dumps(register_message))
        s.sendall(framed_message)

        # Receive server response
        response_data = s.recv(1024)
        try:
            server_message = unframe_websocket_message(response_data)
            print("Received message:", server_message)
        except Exception as e:
            print("Error parsing server response:", e)


# Run the WebSocket client
websocket_communication()
