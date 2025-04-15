from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI()
EVENT_QUEUE = asyncio.Queue()

@app.get("/health")
async def health():
    return {"status": "ok", "name": "Roblex MCP Server"}

@app.get("/events/sse")
async def sse():
    async def event_gen():
        while True:
            event = await EVENT_QUEUE.get()
            yield f"data: {json.dumps(event)}\n\n"
    asyncio.create_task(EVENT_QUEUE.put({"event": "studio:connected"}))
    return StreamingResponse(event_gen(), media_type="text/event-stream")

from fastapi import Request

@app.post("/messages")
async def messages(request: Request):
    data = await request.json()
    msg_type = data.get("type")
    if msg_type == "generate-script":
        description = data.get("description", "")
        # Sinh code Lua mẫu dựa trên mô tả (giả lập)
        code = f"-- Script generated for: {description}\nprint('Hello from Roblex Script!')"
        return {"success": True, "type": "generate-script", "code": code}
    return {"success": False, "error": "Unsupported message type"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
