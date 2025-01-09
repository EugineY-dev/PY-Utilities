import asyncio
import websockets

async def echo_handler(websocket, path):
    print(f"WebSocket connection established from {websocket.remote_address}")

    try:
        async for message in websocket:
            if isinstance(message, bytes):
                print(f"Received binary message: {message}")
                response = b"Echo: " + message
                await websocket.send(response)
                print(f"Sent binary message: {response}")
            else:
                print(f"Received message: {message}")
                response = f"Echo: {message}"
                await websocket.send(response)
                print(f"Sent message: {response}")

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed with error: {e}")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    print("Starting WebSocket server...")
    try:
        async with websockets.serve(
            echo_handler,
            "192.168.0.1",
            8080,
            ping_interval=20,
            ping_timeout=20
        ):
            await asyncio.Future()  # Run forever
    except Exception as e:
        print(f"Failed to start server: {e}")

if __name__ == "__main__":
    asyncio.run(main())
