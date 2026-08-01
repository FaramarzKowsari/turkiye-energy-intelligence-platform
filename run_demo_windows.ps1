$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -e ".[dev,app]"
& ".\.venv\Scripts\python.exe" scripts\generate_demo.py
& ".\.venv\Scripts\python.exe" scripts\build_exports.py
& ".\.venv\Scripts\python.exe" -m pytest
& ".\.venv\Scripts\streamlit.exe" run app\streamlit_app.py
