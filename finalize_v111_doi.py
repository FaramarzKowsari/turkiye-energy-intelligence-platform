from __future__ import annotations

import re
import sys
from pathlib import Path

VERSION = "1.1.1"
VERSION_DOI = "10.5281/zenodo.21763992"
CONCEPT_DOI = "10.5281/zenodo.21749628"
V100_DOI = "10.5281/zenodo.21749629"
V110_DOI = "10.5281/zenodo.21763194"

ROOT = Path(__file__).resolve().parent


def require(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.M | re.S)
    if count != 1:
        raise SystemExit(f"Could not update {label}; expected exactly one match.")
    return updated


def update_citation() -> None:
    path = ROOT / "CITATION.cff"
    require(path)
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^version:\s*.*$", f"version: {VERSION}", text, flags=re.M)
    text = re.sub(
        r'^doi:\s*".*"$',
        f'doi: "{VERSION_DOI}"',
        text,
        flags=re.M,
    )
    path.write_text(text, encoding="utf-8")


def update_readme() -> None:
    path = ROOT / "README.md"
    require(path)
    text = path.read_text(encoding="utf-8")

    citation_block = f'''## Citation

To cite the current archived version `v{VERSION}`:

> Kowsari, Faramarz. (2026). *Türkiye Energy Intelligence Platform* (Version {VERSION}) [Computer software]. Zenodo. https://doi.org/{VERSION_DOI}

Machine-readable citation metadata is available in [`CITATION.cff`](CITATION.cff).

For references to the software project across all current and future versions, use the [Concept DOI](https://doi.org/{CONCEPT_DOI}).

## License'''

    text = replace_once(
        text,
        r"## Citation\s+.*?## License",
        citation_block,
        "README citation section",
    )

    doi_block = f'''<!-- ZENODO_DOI_START -->
### Zenodo DOI

- **All versions / Concept DOI:** [{CONCEPT_DOI}](https://doi.org/{CONCEPT_DOI})
- **Version v1.0.0 DOI:** [{V100_DOI}](https://doi.org/{V100_DOI})
- **Version v1.1.0 DOI:** [{V110_DOI}](https://doi.org/{V110_DOI})
- **Version v{VERSION} DOI:** [{VERSION_DOI}](https://doi.org/{VERSION_DOI})
<!-- ZENODO_DOI_END -->'''

    text = replace_once(
        text,
        r"<!-- ZENODO_DOI_START -->.*?<!-- ZENODO_DOI_END -->",
        doi_block,
        "README Zenodo DOI block",
    )

    path.write_text(text, encoding="utf-8")


def update_website() -> None:
    path = ROOT / "docs" / "index.html"
    require(path)
    text = path.read_text(encoding="utf-8")

    text = replace_once(
        text,
        r'<meta name="citation_doi" content="[^"]+">',
        f'<meta name="citation_doi" content="{VERSION_DOI}">',
        "website citation DOI",
    )
    text = replace_once(
        text,
        r'"version"\s*:\s*"[^"]+"',
        f'"version": "{VERSION}"',
        "website schema version",
    )
    text = replace_once(
        text,
        r'"identifier"\s*:\s*"https://doi\.org/10\.5281/zenodo\.\d+"',
        f'"identifier": "https://doi.org/{VERSION_DOI}"',
        "website schema DOI",
    )

    path.write_text(text, encoding="utf-8")


def update_release_notes() -> None:
    path = ROOT / "RELEASE_NOTES_v1.1.1.md"
    require(path)
    text = path.read_text(encoding="utf-8")

    final_doi_section = f'''## DOI

### Version v{VERSION}

https://doi.org/{VERSION_DOI}

### All Versions / Concept DOI

https://doi.org/{CONCEPT_DOI}

### Previous Version — v1.1.0

https://doi.org/{V110_DOI}
'''

    text = replace_once(
        text,
        r"## DOI\s+.*\Z",
        final_doi_section,
        "release notes DOI section",
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    required = [
        ROOT / "README.md",
        ROOT / "CITATION.cff",
        ROOT / "docs" / "index.html",
        ROOT / "RELEASE_NOTES_v1.1.1.md",
    ]
    for file_path in required:
        require(file_path)

    update_citation()
    update_readme()
    update_website()
    update_release_notes()

    print("DOI finalization completed successfully.")
    print(f"Version: v{VERSION}")
    print(f"Version DOI: {VERSION_DOI}")
    print(f"Concept DOI: {CONCEPT_DOI}")
    print("Updated files:")
    print("- README.md")
    print("- CITATION.cff")
    print("- docs/index.html")
    print("- RELEASE_NOTES_v1.1.1.md")
    print("The repository badge remains linked to the Concept DOI.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
