# ORION-X

A local AI agent with **Grok + Manus + Claude + Emergent** style, powered by your Ollama models.  
GUI included — no API keys, no cloud. Everything runs on your machine.

## Branches

- `main` — stable release
- `ai-bot` — active development

## What You Get

- **Agent personality** combining:
  - **Grok**: Witty, direct, bold
  - **Manus**: Task planning and execution
  - **Claude Pro**: Careful reasoning, structured
  - **Emergent**: Action-oriented, gets results

- **Web GUI** — chat interface with model selector
- **Streaming responses** — see answers as they’re generated
- **100% local** — uses your Ollama (llama2, falcon, gpt-oss, etc.)

## Quick Start

### 1. Make sure Ollama is running

```powershell
ollama serve
```

### 2. Install dependencies

```powershell
cd "c:\Users\mukit\OneDrive\Desktop\privater ai"
pip install -r requirements.txt
```

### 3. Launch the GUI

```powershell
python app.py
```

Or double-click **run.bat** on Windows.

### 4. Open in browser

Go to **http://127.0.0.1:7860**

## Web Version

A standalone web app (HTML/CSS/JS) connected to Ollama:

```powershell
uvicorn web_server:app --host 0.0.0.0 --port 8080
```

Or double-click **run_web.bat**. Then open **http://127.0.0.1:8000**

- Access from other devices on your network (phone, tablet) at `http://YOUR_IP:8000`

## Optional: Custom ORION-X Model

Create a custom Ollama model with the ORION-X personality:

```powershell
ollama create orion-x -f Modelfile
```

Then select `orion-x` in the model dropdown.

## Configuration

Edit `config.py` to:

- Change `DEFAULT_MODEL` (e.g. `gpt-oss:20b` for stronger reasoning)
- Adjust `SYSTEM_PROMPT` to tweak the agent’s behavior

## Next Steps: Full OpenManus

For a more advanced agent (browser automation, code execution, multi-step tasks):

1. Clone [OpenManus](https://github.com/FoundationAgents/OpenManus)
2. Configure `config.toml` to use Ollama
3. Use [OpenManus-GUI](https://github.com/Hank-Chromela/OpenManus-GUI) for a Gradio interface

Requirements: 16GB+ RAM, strong GPU (e.g. RTX 4090) for best performance.

## Project Structure

```
ORION-X/
├── app.py          # Gradio UI
├── web_server.py   # Web app (FastAPI + HTML)
├── web/            # Web frontend
│   ├── index.html
│   ├── style.css
│   └── app.js
├── agent.py        # Ollama chat logic
├── config.py       # Settings & system prompt
├── Modelfile       # Custom Ollama model (optional)
├── run.bat         # Gradio launcher
├── run_web.bat     # Web launcher
├── requirements.txt
└── README.md
```
