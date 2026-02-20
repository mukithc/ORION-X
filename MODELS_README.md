# ORION-X Model Guide

## Why Not All "Free" Models?

The models you listed include **229B, 403B, 754B, and 1T parameter** models. These need **100GB+ VRAM** and won't run on consumer PCs. We include only models that fit on 8–24GB systems.

## Download Practical Models

**Option 1: Double-click `download_models.bat`**

**Option 2: Manual**
```powershell
ollama pull llama3.2:3b
ollama pull mistral:7b
ollama pull qwen2.5:7b
# etc.
```

## Models Included

| Model | Size | Use |
|-------|------|-----|
| llama3.2:3b | 2GB | Fast chat |
| llama3.2:1b | 1.3GB | Very fast |
| mistral:7b | 4.1GB | Strong 7B |
| phi3:mini | 2.3GB | Efficient |
| qwen2.5:7b | 4.7GB | Reasoning |
| gemma2:2b | 1.6GB | Small |
| deepseek-r1:1.5b | 1GB | Reasoning |
| codellama:7b | 4.3GB | Code |
| nomic-embed-text | 274MB | Embeddings |

## Hugging Face Models

1. Enable at: https://huggingface.co/settings/local-apps
2. Run:
```powershell
ollama run hf.co/Nanbeige/Nanbeige4.1-3B
ollama run hf.co/openbmb/MiniCPM-SALA
```

## Large Models (Enterprise Only)

| Model | Params | VRAM Needed |
|-------|--------|-------------|
| MiniMax-M2.5 | 229B | ~120GB+ |
| Qwen3.5-397B | 403B | ~200GB+ |
| GLM-5 | 754B | ~400GB+ |
| Ring-2.5 | 1T | ~500GB+ |
| Kimi-K2.5 | 171B | ~90GB+ |

Use cloud APIs (Groq, Together, etc.) for these.
