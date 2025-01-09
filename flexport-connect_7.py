import websocket
import json
import requests

# REST API configuration
REST_API_BASE_URL = "http://192.168.0.101:61630/test"
GENERATE_TICKET_URL = f"{REST_API_BASE_URL}/createTicket"
CHECK_TICKET_STATE_URL = f"{REST_API_BASE_URL}/getTicketInfo"

# Generate a barcode ticket
def generate_ticket(amount, pin):
    params = {"amount": amount, "pin": pin}
    print("Generating barcode ticket...")
    response = requests.get(GENERATE_TICKET_URL, params=params)
    if response.status_code == 200:
        ticket_info = response.json()
        print("Ticket generated:", ticket_info)
        return ticket_info["number"]
    else:
        print("Failed to generate ticket:", response.status_code, response.text)
        return None

# Check the state of a ticket
def check_ticket_state(ticket_number):
    params = {"ticketNum": ticket_number}
    print("Checking ticket state...")
    response = requests.get(CHECK_TICKET_STATE_URL, params=params)
    if response.status_code == 200:
        ticket_state = response.json()
        print("Ticket state:", ticket_state)
        return ticket_state
    else:
        print("Failed to check ticket state:", response.status_code, response.text)
        return None

# WebSocket callbacks
def on_message(ws, message):
    print("Received message:", message)
    response_data = json.loads(message)

    # Handle WebSocket responses
    message_type = response_data.get("data", {}).get("messageType")
    if message_type == "REGISTER_FLEX_PORT_CLIENT_REPLY":
        print("Device successfully registered. Ready for further transactions.")
        # Proceed with WebSocket communication here if needed
    elif message_type == "ERROR":
        error_message = response_data.get("data", {}).get("errorMessage", "Unknown error.")
        code = response_data.get("data", {}).get("code", "Unknown code.")
        print(f"Error occurred: {error_message} (Code: {code})")
    else:
        print("Unexpected response:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Closed connection")

def on_open(ws):
    # Register the device on WebSocket connection open
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
        }
    }
    ws.send(json.dumps(register_message))

# Main flow
if __name__ == "__main__":
    # Generate a barcode ticket
    ticket_number = generate_ticket(amount=55, pin=7777)
    if not ticket_number:
        print("Failed to generate a ticket. Exiting.")
        exit()

    # Check the state of the ticket
    ticket_state = check_ticket_state(ticket_number)
    if not ticket_state or ticket_state.get("playableAmount", 0) <= 0:
        print("Invalid or unusable ticket. Exiting.")
        exit()

    # Proceed with WebSocket communication
    websocket_url = "ws://192.168.0.101:61630/ws/flexpay/client/v1/communication"
    ws = websocket.WebSocketApp(websocket_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()
