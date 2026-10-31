
@echo off
title PeerTutor AI Launcher

echo Starting PeerTutor AI...

echo Checking Ollama...
ollama list

echo Starting Backend...
start "PeerTutor Backend" cmd /k "cd /d %~dp0backend && %~dp0venv\Scripts\python.exe -m uvicorn server:app --host 127.0.0.1 --port 8001"

timeout /t 5 /nobreak

echo Starting Frontend...
start "PeerTutor Frontend" cmd /k "cd /d %~dp0 && %~dp0venv\Scripts\python.exe -m streamlit run streamlit_app.py"

echo.
echo Both services launched!
pause
