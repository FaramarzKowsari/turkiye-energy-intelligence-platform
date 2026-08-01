from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from .base import EnergyDataProvider


class LocalFileProvider(EnergyDataProvider):
    name = "local"

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def fetch(self, start: datetime | None = None, end: datetime | None = None) -> pd.DataFrame:
        suffix = self.path.suffix.lower()
        if suffix == ".csv":
            frame = pd.read_csv(self.path)
        elif suffix in {".xlsx", ".xls"}:
            frame = pd.read_excel(self.path)
        elif suffix == ".parquet":
            frame = pd.read_parquet(self.path)
        else:
            raise ValueError(f"Unsupported local file type: {suffix}")
        if "timestamp" not in frame:
            raise ValueError("Local data must contain a timestamp column")
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="raise")
        if start is not None:
            frame = frame[frame["timestamp"] >= pd.Timestamp(start)]
        if end is not None:
            frame = frame[frame["timestamp"] <= pd.Timestamp(end)]
        return frame.reset_index(drop=True)
