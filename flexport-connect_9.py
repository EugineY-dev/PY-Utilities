import websocket
import json

# Callback functions for WebSocket events
def on_message(ws, message):
    print("Received message:", message)
    response_data = json.loads(message)

    # Handle different message types based on server response
    if response_data.get("data", {}).get("messageType") == "REGISTER_FLEX_PORT_CLIENT_REPLY":
        print("Device successfully registered. Ready for further transactions.")
        # Proceed with further requests here (e.g., check ticket existence)
        check_ticket_existence(ws)  # Example function call after registration
    else:
        print("Unexpected response or registration failed.")

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Closed connection")

def on_open(ws):
    # Register the device on open connection
    register_device(ws)

def register_device(ws):
    # Constructing the device registration message
    register_message = {
        "timestamp": 1721124745135,  # Example timestamp; replace as needed
        "version": 1,
        "token": "c5287677-4b7a-4f31-acd5-5e5ddf023c76",  # Replace with your token
        "data": {
            "messageType": "REGISTER_FLEX_PORT_CLIENT",
            "deviceId": "230E568803000093",  # Replace with your deviceId
            "softwareVersion": "GCOAM-1.14.x.4.3.1.SNAPSHOT"  # Replace with your software version
            # "softwareVersion": "GCOAM-1.14.x.4.3.1.SNAPSHOT"
        }
    }
    # Send the registration message as a JSON string
    buf = json.dumps(register_message)
    ws.send(buf)
    print("Message sent: ", buf)

def check_ticket_existence(ws):
    # Example function to send a ticket existence check request after registration
    request_message = {
        "timestamp": 1721977276211,  # Example timestamp; replace as needed
        "version": 1,
        "token": "4fccbefb-9011-482b-8a20-fc610ba207e3",  # Replace with your token
        "data": {
            "messageType": "CHECK_TICKET_EXISTENCE",
            # "ticketNumber": "172182202022221610"  # Replace as needed
            "ticketNumber": "171948419023919622"  # Replace as needed
        }
    }
    ws.send(json.dumps(request_message))

# Set the WebSocket URL (replace with your server's IP address)
# websocket_url = "ws://192.168.0.101:61630/ws/flexpay/client/v1/communication"
websocket_url = "ws://192.168.0.100:61630/ws/flexpay/client/v1/communication"

# Create and configure the WebSocket connection
ws = websocket.WebSocketApp(websocket_url,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

# Run the WebSocket client
ws.run_forever()
