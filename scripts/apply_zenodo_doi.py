from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOI_RE = re.compile(r"^10\.5281/zenodo\.\d+$")


def replace_block(path: Path, start: str, end: str, body: str) -> None:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    replacement = f"{start}\n{body}\n{end}"
    if not pattern.search(text):
        raise RuntimeError(f"DOI marker block missing in {path}")
    path.write_text(pattern.sub(replacement, text), encoding="utf-8")


def main(doi: str) -> None:
    doi = doi.strip().removeprefix("https://doi.org/")
    if not DOI_RE.fullmatch(doi):
        raise SystemExit("Expected a Zenodo DOI such as 10.5281/zenodo.12345678")

    citation = ROOT / "CITATION.cff"
    cff = citation.read_text(encoding="utf-8")
    if re.search(r"^doi:", cff, flags=re.M):
        cff = re.sub(r"^doi:.*$", f'doi: "{doi}"', cff, flags=re.M)
    else:
        cff += f'\ndoi: "{doi}"\n'
    citation.write_text(cff, encoding="utf-8")

    zenodo_path = ROOT / ".zenodo.json"
    metadata = json.loads(zenodo_path.read_text(encoding="utf-8"))
    metadata["doi"] = doi
    serialized = json.dumps(metadata, ensure_ascii=False, indent=2) + "\n"
    zenodo_path.write_text(serialized, encoding="utf-8")

    badge = f"[![DOI](https://zenodo.org/badge/DOI/{doi}.svg)](https://doi.org/{doi})"
    replace_block(
        ROOT / "README.md",
        "<!-- ZENODO_DOI_START -->",
        "<!-- ZENODO_DOI_END -->",
        badge,
    )

    site = ROOT / "docs/index.html"
    html = site.read_text(encoding="utf-8")
    tag = f'<meta name="citation_doi" content="{doi}">'
    if 'name="citation_doi"' in html:
        html = re.sub(r'<meta name="citation_doi" content="[^"]+">', tag, html)
    else:
        anchor = '<meta name="author" content="Faramarz Kowsari">'
        html = html.replace(anchor, f"{anchor}\n  {tag}")
    site.write_text(html, encoding="utf-8")
    print(f"Applied DOI {doi} to citation metadata, README and website.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python scripts/apply_zenodo_doi.py 10.5281/zenodo.YOUR_ID"
        )
    main(sys.argv[1])
