import asyncio
import websockets
from datetime import datetime


async def handler(websocket, path):
    print(f"WebSocket connection established at {datetime.now()}")
    try:
        # You won't see the HTTP handshake here because websockets abstracts that away,
        # but we can handle the messages.
        while True:
            message = await websocket.recv()
            print(f"Received from STM32: {message}")

            # Send a response back to STM32
            response = "Hello from PC"
            await websocket.send(response)
            print(f"Sent to STM32: {response}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"WebSocket connection closed with error: {e}")

# Start WebSocket server on ws://localhost:8080
start_server = websockets.serve(handler, "0.0.0.0", 8080)

print("Starting WebSocket server...")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
