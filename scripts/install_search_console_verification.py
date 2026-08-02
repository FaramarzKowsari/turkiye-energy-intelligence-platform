from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main(source: str) -> None:
    src = Path(source).expanduser().resolve()
    if not src.exists() or not src.is_file():
        raise SystemExit(f"Verification file not found: {src}")
    if not src.name.startswith("google") or src.suffix.lower() != ".html":
        raise SystemExit(
            "Use the exact google*.html file downloaded from Google Search Console."
        )

    target = ROOT / "docs" / src.name
    shutil.copyfile(src, target)
    print(f"Installed unchanged: {target.relative_to(ROOT)}")
    print("Commit and push this file, wait for GitHub Pages deployment, then verify.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python scripts/install_search_console_verification.py "
            "PATH_TO_GOOGLE_HTML"
        )
    main(sys.argv[1])
