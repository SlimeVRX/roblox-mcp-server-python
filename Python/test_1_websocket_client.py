import asyncio
import websockets

async def websocket_client():
    uri = "ws://localhost:8001/ws/testclient"
    async with websockets.connect(uri) as websocket:
        print("[WebSocket] Connected as testclient")

        # Gửi thử 1 message
        await websocket.send('{"msg": "Hello Relay!"}')
        print("[WebSocket] Sent initial message.")

        # Lắng nghe từ server
        while True:
            try:
                message = await websocket.recv()
                print("[WebSocket] Received:", message)
            except websockets.ConnectionClosed:
                print("[WebSocket] Connection closed.")
                break

asyncio.run(websocket_client())
