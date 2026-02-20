"""
ORION-X Web Server
Serves a web chat UI connected to your local Ollama.
"""

import json
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agent import chat, get_available_models
from config import DEFAULT_MODEL, OLLAMA_HOST
from tools import process_with_tools

app = FastAPI(title="ORION-X", version="1.0")

# Serve static files from web/ folder
WEB_DIR = Path(__file__).parent / "web"
if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


class ChatRequest(BaseModel):
    message: str
    model: str = DEFAULT_MODEL
    history: list[dict] = []


@app.get("/")
async def index():
    """Serve the chat UI."""
    index_path = WEB_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "ORION-X API. Add web/index.html for UI.", "docs": "/docs"}


@app.get("/api/models")
async def list_models():
    """List available Ollama models."""
    try:
        models = get_available_models()
        return {"models": models, "default": DEFAULT_MODEL}
    except Exception as e:
        return {"models": [], "error": str(e)}


@app.post("/api/chat")
async def chat_stream(request: ChatRequest):
    """Stream chat response from Ollama."""

    def generate():
        messages = []
        for h in request.history:
            role = h.get("role", "user")
            content = h.get("content", "")
            if isinstance(content, list) and content:
                content = content[0].get("text", "") if isinstance(content[0], dict) else ""
            messages.append({"role": role, "content": str(content)})
        final_message = process_with_tools(request.message)
        messages.append({"role": "user", "content": final_message})

        for chunk in chat(messages, model=request.model, stream=True):
            yield f"data: {json.dumps({'content': chunk})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
