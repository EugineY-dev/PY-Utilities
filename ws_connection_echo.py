import asyncio
import websockets


async def echo(websocket, path):
    print(f"WebSocket connection established from {websocket.remote_address}")
    try:
        while True:
            # Wait for a message from the STM32
            message = await websocket.recv()
            print(f"Received message: {message}")

            # Echo back the received message
            response = f"Echo: {message}"
            await websocket.send(response)
            print(f"Sent back: {response}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"WebSocket connection closed: {e}")


async def main():
    print("Starting WebSocket server...")  # Add visibility here
    async with websockets.serve(echo, "0.0.0.0", 8080):
        await asyncio.Future()  # run forever

asyncio.run(main())
