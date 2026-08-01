from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "LICENSE", "CITATION.cff", ".zenodo.json", "CHANGELOG.md",
    "docs/index.html", "docs/robots.txt", "docs/sitemap.xml",
    "data/samples/energy_hourly_demo.csv", "pyproject.toml",
]


def main() -> None:
    errors: list[str] = []
    for item in REQUIRED:
        if not (ROOT / item).exists():
            errors.append(f"Missing required file: {item}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    site = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    for token in ("English", "Türkçe", "Faramarz Kowsari", "EPİAŞ", "TEİAŞ"):
        if token not in readme:
            errors.append(f"README missing token: {token}")
    for token in ('data-lang="en"', 'data-lang="tr"', "application/ld+json", "sitemap.xml"):
        if token not in site:
            errors.append(f"Site missing token: {token}")

    metadata = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    if metadata.get("creators", [{}])[0].get("orcid") != "0000-0003-1692-0453":
        errors.append("Zenodo ORCID is missing or incorrect")

    result = subprocess.run(
        [sys.executable, "-m", "compileall", "-q", "src", "app", "scripts"],
        cwd=ROOT,
        check=False,
    )
    if result.returncode:
        errors.append("Python compile audit failed")

    if errors:
        print("RELEASE AUDIT FAILED")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("RELEASE AUDIT PASSED")
    print(f"Required files: {len(REQUIRED)}")
    print("Bilingual README/site, author metadata, SEO files and Zenodo metadata: present")


if __name__ == "__main__":
    main()
