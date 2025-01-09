import websocket
import json

# Callback functions for WebSocket events
def on_message(ws, message):
    print("Received message:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Closed connection")

def on_open(ws):
    # JSON message to be sent as per your protocol
    request_message = {
        "timestamp": 1721977276211,  # Example timestamp; replace as needed
        "version": 1,
        "token": "4fccbefb-9011-482b-8a20-fc610ba207e3",  # Replace as needed
        "data": {
            "messageType": "CHECK_TICKET_EXISTENCE",
            "ticketNumber": "172182202022221610"  # Replace as needed
        }
    }
    # Send the message as a JSON string
    ws.send(json.dumps(request_message))

# Set the WebSocket URL (replace IP with your server address)
websocket_url = "ws://192.168.0.101:61630/ws/flexpay/client/v1/communication"

# Create and configure WebSocket connection
ws = websocket.WebSocketApp(websocket_url,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

# Run the WebSocket client
ws.run_forever()
