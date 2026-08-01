@echo off
if not exist "%~dp0.venv\Scripts\uvicorn.exe" (
  echo Run run_demo_windows.bat once to install dependencies.
  exit /b 1
)
cd /d "%~dp0"
.venv\Scripts\uvicorn.exe enerjinabiz.api:app --host 127.0.0.1 --port 8000
