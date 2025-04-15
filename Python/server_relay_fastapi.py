from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from fastapi import Request

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = {}  # client_id -> websocket
message_queues = {}  # client_id -> asyncio.Queue()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    print(f"[CONNECTED] {client_id}")
    clients[client_id] = websocket
    message_queues[client_id] = asyncio.Queue()
    try:
        while True:
            message = await websocket.receive_text()
            print(f"[RECEIVED from {client_id}] {message}")
            # Store the message for polling
            await message_queues[client_id].put(message)
    except WebSocketDisconnect:
        print(f"[DISCONNECTED] {client_id}")
        clients.pop(client_id, None)
        message_queues.pop(client_id, None)

@app.get("/api/poll/{client_id}")
async def poll(client_id: str):
    queue = message_queues.get(client_id)
    if not queue:
        return JSONResponse(content={"message": None})
    try:
        msg = await asyncio.wait_for(queue.get(), timeout=1)
        return JSONResponse(content={"message": msg})
    except asyncio.TimeoutError:
        return JSONResponse(content={"message": None})

@app.post("/api/send/{client_id}")
async def send(client_id: str, request: Request):
    if client_id not in clients:
        return JSONResponse(content={"error": "client not connected"}, status_code=400)
    body = await request.body()
    msg = body.decode()
    try:
        await clients[client_id].send_text(msg)
        return JSONResponse(content={"success": True})
    except:
        return JSONResponse(content={"success": False}, status_code=500)

@app.get("/health")
async def health():
    return {"status": "ok", "relay": "fastapi"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server_relay_fastapi:app", host="0.0.0.0", port=8001, reload=False)