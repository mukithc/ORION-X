"""Agent logic - connects to Ollama with Grok/Manus/Claude/Emergent style."""

import json
import re
from typing import Generator

import ollama
from ollama import Client

from config import OLLAMA_HOST, DEFAULT_MODEL, SYSTEM_PROMPT


def get_available_models() -> list[str]:
    """Fetch models from Ollama."""
    try:
        client = Client(host=OLLAMA_HOST)
        resp = client.list()
        # Handle both object and dict response
        models = getattr(resp, "models", resp.get("models", []))
        return [getattr(m, "model", m.get("model", "")) for m in models]
    except Exception:
        return ["llama2:latest", "falcon:latest", "gpt-oss:20b"]


def chat(
    messages: list[dict],
    model: str = DEFAULT_MODEL,
    stream: bool = True,
) -> Generator[str, None, None]:
    """Stream chat response from Ollama with agent system prompt."""
    client = Client(host=OLLAMA_HOST)

    # Prepend system prompt if not already in messages
    if not messages or messages[0].get("role") != "system":
        full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    else:
        full_messages = messages

    if stream:
        stream_obj = client.chat(
            model=model,
            messages=full_messages,
            stream=True,
        )
        for chunk in stream_obj:
            msg = getattr(chunk, "message", chunk.get("message", {}))
            content = getattr(msg, "content", msg.get("content", "")) if msg else ""
            if content:
                yield content
    else:
        response = client.chat(model=model, messages=full_messages)
        msg = getattr(response, "message", response.get("message", {}))
        yield getattr(msg, "content", msg.get("content", "")) or ""


def _extract_content(content) -> str:
    """Extract text from Gradio/OpenAI content format."""
    if isinstance(content, str):
        return content
    if isinstance(content, list) and content:
        return content[0].get("text", "") if isinstance(content[0], dict) else str(content[0])
    return ""


def chat_simple(
    user_message: str,
    history: list,
    model: str = DEFAULT_MODEL,
) -> Generator[str, None, None]:
    """Simple chat for Gradio - converts history to messages."""
    messages = []
    for h in history or []:
        if isinstance(h, dict):
            role = h.get("role", "user")
            content = _extract_content(h.get("content", ""))
            messages.append({"role": role, "content": content})
        else:
            user, assistant = h[0], h[1] if len(h) > 1 else ""
            messages.append({"role": "user", "content": str(user)})
            messages.append({"role": "assistant", "content": str(assistant)})
    messages.append({"role": "user", "content": user_message})

    yield from chat(messages, model=model, stream=True)
