# ORION-X Model Guide

## Download All Open-Source Models

**Option 1: `download_all_models.bat`** — Double-click to run

**Option 2: Python**
```powershell
python download_all_models.py
```
- Choice 1: Ollama native only
- Choice 2: Ollama + Hugging Face (enable HF Ollama first)
- Choice 3: Hugging Face only

**Hugging Face setup:** https://huggingface.co/settings/local-apps → enable Ollama

## Models Included (Open Source Only)

### Ollama Native
| Model | Size |
|-------|------|
| llama3.2:3b, llama3.2:1b | 2GB, 1.3GB |
| mistral:7b, phi3:mini | 4.1GB, 2.3GB |
| qwen2.5:7b, gemma2:2b | 4.7GB, 1.6GB |
| deepseek-r1:1.5b | 1GB |
| codellama:7b, qwen2.5-coder:7b | 4.3GB |
| llama3.1:8b | 4.7GB |
| nomic-embed-text | 274MB |

### Hugging Face GGUF
| Model | Params |
|-------|--------|
| Nanbeige4.1-3B, QED-Nano | 4B |
| MiniCPM-SALA, MiniCPM-o-4_5 | 8-9B |
| Nemotron-Nano-9B-Japanese | 9B |
| gpt-oss-20b-GGUF | 21B |
| GLM-4.7-Flash-REAP-23B | 23B |
| GLM-4.7-Flash, Qwen3-Coder-30B | 30-31B |

## Skipped (Too Large / Not Open)

- **229B+** (MiniMax-M2.5, Qwen3.5-397B, GLM-5, Kimi-K2.5) — need 100GB+ VRAM
- **1T** (Ring-2.5, Ling-2.5) — enterprise only
- **Proprietary** — use cloud APIs instead
