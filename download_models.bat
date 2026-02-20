@echo off
echo ORION-X - Downloading free Ollama models...
echo.
echo These models fit on 8-16GB VRAM systems.
echo Large models (229B, 403B, 754B) need 100GB+ - skipped.
echo.

ollama pull llama3.2:3b
ollama pull llama3.2:1b
ollama pull mistral:7b
ollama pull phi3:mini
ollama pull qwen2.5:7b
ollama pull gemma2:2b
ollama pull deepseek-r1:1.5b
ollama pull codellama:7b
ollama pull nomic-embed-text

echo.
echo Done! Run 'ollama list' to see your models.
pause
