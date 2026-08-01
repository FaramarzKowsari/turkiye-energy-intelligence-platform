from __future__ import annotations

from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

from .base import EnergyDataProvider


class TeiasCatalogProvider(EnergyDataProvider):
    """Discovers public TEİAŞ sector-report links.

    TEİAŞ report formats can change. This provider intentionally returns a catalog
    rather than pretending every report has one stable machine-readable schema.
    """

    name = "teias-catalog"
    catalog_url = "https://www.teias.gov.tr/aylik-elektrik-uretim-tuketim-raporlari"

    def fetch(self, start: datetime | None = None, end: datetime | None = None) -> pd.DataFrame:
        response = requests.get(self.catalog_url, timeout=45)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        rows: list[dict[str, str]] = []
        for link in soup.find_all("a", href=True):
            text = " ".join(link.get_text(" ", strip=True).split())
            href = link["href"]
            if "Üretim" in text or "Tüketim" in text or "uretim" in href.lower():
                if href.startswith("/"):
                    href = "https://www.teias.gov.tr" + href
                rows.append({"title": text or "TEİAŞ report", "url": href, "source": "teias"})
        return pd.DataFrame(rows).drop_duplicates().reset_index(drop=True)
