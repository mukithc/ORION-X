# Private AI Agent

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

### 4. Open in browser

Go to **http://127.0.0.1:7860**

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

## Push to GitHub

1. Create a new repo at [github.com/new](https://github.com/new) (e.g. `privater-ai` or `private-ai-agent`)
2. Run:

```powershell
cd "c:\Users\mukit\OneDrive\Desktop\privater ai"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
git push -u origin ai-bot
```
