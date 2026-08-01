from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone
from typing import Any

import pandas as pd
import requests

from enerjinabiz.exceptions import ProviderConfigurationError, ProviderResponseError
from enerjinabiz.providers.base import EnergyDataProvider


class EpiasProvider(EnergyDataProvider):
    """Optional authenticated EPİAŞ electricity-service provider.

    This adapter uses documented endpoints and keeps credentials local. It is
    isolated from the analytics layer so API changes do not break demo or local
    execution.
    """

    name = "epias"

    def __init__(
        self,
        username: str | None,
        password: str | None,
        base_url: str = "https://seffaflik.epias.com.tr/electricity-service",
        auth_url: str = "https://giris.epias.com.tr/cas/v1/tickets",
        timeout: int = 45,
    ) -> None:
        if not username or not password:
            raise ProviderConfigurationError(
                "EPİAŞ credentials are missing. Set EPIAS_USERNAME and "
                "EPIAS_PASSWORD locally."
            )
        self.username = username
        self.password = password
        self.base_url = base_url.rstrip("/")
        self.auth_url = auth_url
        self.timeout = timeout
        self.session = requests.Session()
        self._tgt: str | None = None
        self._tgt_expires_at = 0.0

    @staticmethod
    def _fmt(value: datetime) -> str:
        """Format a timestamp in the +03:00 format documented by EPİAŞ."""
        if value.tzinfo is None:
            return value.strftime("%Y-%m-%dT%H:%M:%S+03:00")
        istanbul_tz = timezone(timedelta(hours=3))
        return value.astimezone(istanbul_tz).isoformat(timespec="seconds")

    def _get_tgt(self) -> str:
        if self._tgt and time.time() < self._tgt_expires_at:
            return self._tgt
        response = self.session.post(
            self.auth_url,
            data={"username": self.username, "password": self.password},
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "text/plain",
            },
            timeout=self.timeout,
        )
        if response.status_code != 201 or not response.text.strip().startswith("TGT-"):
            raise ProviderResponseError(
                f"EPİAŞ authentication failed: HTTP {response.status_code}. "
                "Check the local account credentials; they are never stored."
            )
        self._tgt = response.text.strip()
        # Official TGT lifetime is two hours; refresh early to avoid expiry.
        self._tgt_expires_at = time.time() + 100 * 60
        return self._tgt

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}{path}",
            json=payload,
            headers={"TGT": self._get_tgt(), "Accept": "application/json"},
            timeout=self.timeout,
        )
        if response.status_code >= 400:
            excerpt = response.text[:300]
            raise ProviderResponseError(
                f"EPİAŞ endpoint {path} failed: HTTP {response.status_code} - {excerpt}"
            )
        try:
            data = response.json()
        except requests.JSONDecodeError as exc:
            raise ProviderResponseError(
                f"EPİAŞ endpoint {path} returned invalid JSON"
            ) from exc
        if not isinstance(data, dict):
            raise ProviderResponseError(f"Unexpected EPİAŞ response type for {path}")
        return data

    @staticmethod
    def _items(payload: dict[str, Any]) -> list[dict[str, Any]]:
        """Accept documented top-level items and common envelope wrappers."""
        candidates = (
            payload,
            payload.get("body"),
            payload.get("data"),
            payload.get("result"),
        )
        for candidate in candidates:
            if isinstance(candidate, dict) and isinstance(candidate.get("items"), list):
                return [item for item in candidate["items"] if isinstance(item, dict)]
        return []

    @staticmethod
    def _timestamp(frame: pd.DataFrame) -> pd.DataFrame:
        if frame.empty:
            return frame
        source = None
        if "date" in frame.columns:
            source = "date"
        elif "timestamp" in frame.columns:
            source = "timestamp"
        if source is None:
            return frame
        frame = frame.copy()
        parsed = pd.to_datetime(frame[source], errors="coerce", utc=True)
        frame["timestamp"] = parsed.dt.tz_convert("Europe/Istanbul").dt.tz_localize(None)
        return frame

    def fetch(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> pd.DataFrame:
        # Avoid the latest incomplete consumption window, which is published
        # with a documented delay.
        end = end or datetime.now() - timedelta(hours=3)
        start = start or end - timedelta(days=7)
        if start >= end:
            raise ValueError("start must be earlier than end")
        body = {"startDate": self._fmt(start), "endDate": self._fmt(end)}

        consumption_payload = self._post(
            "/v1/consumption/data/realtime-consumption",
            body,
        )
        generation_payload = self._post(
            "/v1/generation/data/realtime-generation",
            body,
        )
        price_payload = self._post("/v1/markets/dam/data/mcp", body)

        cdf = self._timestamp(pd.DataFrame(self._items(consumption_payload)))
        gdf = self._timestamp(pd.DataFrame(self._items(generation_payload)))
        pdf = self._timestamp(pd.DataFrame(self._items(price_payload)))
        if cdf.empty or "timestamp" not in cdf.columns:
            raise ProviderResponseError("EPİAŞ returned no usable consumption records")

        cdf = cdf.rename(columns={"consumption": "consumption_mwh"})
        pdf = pdf.rename(columns={"price": "market_price_try_mwh"})
        consumption_columns = [
            column
            for column in ["timestamp", "consumption_mwh"]
            if column in cdf
        ]
        merged = cdf[consumption_columns].dropna(subset=["timestamp"])

        price_columns = {"timestamp", "market_price_try_mwh"}
        if price_columns.issubset(pdf.columns):
            price_data = pdf[["timestamp", "market_price_try_mwh"]]
            merged = merged.merge(
                price_data.drop_duplicates("timestamp"),
                on="timestamp",
                how="left",
            )

        if "blackCoal" in gdf.columns or "hardCoal" in gdf.columns:
            black = None
            hard = None
            if "blackCoal" in gdf:
                black = pd.to_numeric(gdf.get("blackCoal"), errors="coerce")
            if "hardCoal" in gdf:
                hard = pd.to_numeric(gdf.get("hardCoal"), errors="coerce")
            if black is not None and hard is not None:
                gdf["hard_coal_mwh"] = black.combine_first(hard)
            elif black is not None:
                gdf["hard_coal_mwh"] = black
            elif hard is not None:
                gdf["hard_coal_mwh"] = hard

        generation_map = {
            "naturalGas": "natural_gas_mwh",
            "lignite": "lignite_mwh",
            "importCoal": "imported_coal_mwh",
            "river": "run_of_river_mwh",
            "dammedHydro": "dam_hydro_mwh",
            "wind": "wind_mwh",
            "sun": "solar_mwh",
            "geothermal": "geothermal_mwh",
            "biomass": "biomass_mwh",
            "wasteheat": "waste_heat_mwh",
            "importExport": "import_export_mwh",
            "asphaltiteCoal": "asphaltite_coal_mwh",
            "fueloil": "fuel_oil_mwh",
            "lng": "lng_mwh",
            "naphta": "naphtha_mwh",
            "total": "generation_mwh",
        }
        if not gdf.empty and "timestamp" in gdf.columns:
            gdf = gdf.rename(columns=generation_map)
            generation_columns = ["timestamp", "hard_coal_mwh"]
            generation_columns.extend(
                column
                for column in generation_map.values()
                if column in gdf.columns
            )
            keep = list(
                dict.fromkeys(
                    column for column in generation_columns if column in gdf.columns
                )
            )
            generation_data = gdf[keep].drop_duplicates("timestamp")
            merged = merged.merge(generation_data, on="timestamp", how="left")

        merged["source"] = "epias"
        merged["is_synthetic"] = False
        return merged.sort_values("timestamp").reset_index(drop=True)
