from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
required = [
    ROOT / "app/streamlit_app.py",
    ROOT / "requirements.txt",
    ROOT / ".streamlit/secrets.toml.example",
    ROOT / "docs/EPIAS_LIVE_SETUP.md",
]

missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
if missing:
    raise SystemExit("Missing files: " + ", ".join(missing))

ast.parse((ROOT / "app/streamlit_app.py").read_text(encoding="utf-8"))
requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
for package in ("streamlit", "pandas", "plotly", "requests", "numpy"):
    if package not in requirements:
        raise SystemExit(f"Missing dependency: {package}")

print("EPİAŞ live-mode pack validation passed.")
