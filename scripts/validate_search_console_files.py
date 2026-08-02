from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
EXPECTED = {"robots.txt", "sitemap.xml", "index.html", "404.html"}

missing = sorted(name for name in EXPECTED if not (DOCS / name).exists())
if missing:
    raise SystemExit("Missing required files: " + ", ".join(missing))

robots = (DOCS / "robots.txt").read_text(encoding="utf-8")
expected_sitemap = "https://faramarzkowsari.github.io/turkiye-energy-intelligence-platform/sitemap.xml"
if "User-agent: *" not in robots or "Allow: /" not in robots:
    raise SystemExit("robots.txt does not allow crawling.")
if expected_sitemap not in robots:
    raise SystemExit("robots.txt does not point to the canonical sitemap.")

tree = ET.parse(DOCS / "sitemap.xml")
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [node.text.strip() for node in tree.findall(".//sm:loc", ns) if node.text]
if "https://faramarzkowsari.github.io/turkiye-energy-intelligence-platform/" not in urls:
    raise SystemExit("Canonical homepage is missing from sitemap.xml.")

index = (DOCS / "index.html").read_text(encoding="utf-8")
checks = {
    "canonical": '<link rel="canonical" href="https://faramarzkowsari.github.io/turkiye-energy-intelligence-platform/">',
    "robots meta": 'name="robots"',
    "description": 'name="description"',
    "structured data": 'application/ld+json',
}
failed = [name for name, needle in checks.items() if needle not in index]
if failed:
    raise SystemExit("index.html missing: " + ", ".join(failed))

verification_files = sorted(DOCS.glob("google*.html"))
print("Search Console file validation passed.")
print("Sitemap URLs:", urls)
if verification_files:
    print("Google verification file:", verification_files[0].name)
else:
    print("Google verification file not installed yet.")
