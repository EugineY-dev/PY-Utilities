import asyncio
import websockets


async def handle_websocket(websocket, path):
    print(f"WebSocket connection established from {websocket.remote_address}")

    try:
        async for message in websocket:
            print(f"Received message: {message}")
    except websockets.ConnectionClosed:
        print("Connection closed")


start_server = websockets.serve(handle_websocket, "0.0.0.0", 8080)

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server started...")
asyncio.get_event_loop().run_forever()
