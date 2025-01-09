import websocket
import json


def on_message(ws, message):
    print("Received:", message)


def on_error(ws, error):
    print("Error:", error)


def on_close(ws, close_status_code, close_msg):
    print("Closed connection:", close_msg)


def on_open(ws):
    # Construct the JSON message as per the protocol
    request_message = {
        "timestamp": 1721977276211,  # Example timestamp; replace as needed
        "version": 1,
        "token": "4fccbefb-9011-482b-8a20-fc610ba207e3",  # Replace as needed
        "data": {
            "messageType": "CHECK_TICKET_EXISTENCE",
            "ticketNumber": "172182202022221610"  # Replace as needed
        }
    }
    # Send the message
    ws.send(json.dumps(request_message))


# Replace ws://192.168.0.101:61630 with the appropriate WebSocket server URL
websocket_url = "ws://192.168.0.101:61630/ws/flexpay/client/v1/communication"

# Connect to the WebSocket server
ws = websocket.WebSocketApp(websocket_url,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

# Run the WebSocket client
ws.run_forever()
