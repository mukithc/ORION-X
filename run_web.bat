@echo off
echo Starting ORION-X Web Server...
echo.
echo Make sure Ollama is running: ollama serve
echo.
echo Open in browser: http://127.0.0.1:8000
echo.
uvicorn web_server:app --host 0.0.0.0 --port 8000 --reload
pause
