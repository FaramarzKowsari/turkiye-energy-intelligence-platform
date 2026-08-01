from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from .base import EnergyDataProvider


class DemoProvider(EnergyDataProvider):
    name = "demo"

    def __init__(self, path: str | Path = "data/samples/energy_hourly_demo.csv") -> None:
        self.path = Path(path)

    def fetch(self, start: datetime | None = None, end: datetime | None = None) -> pd.DataFrame:
        if not self.path.exists():
            raise FileNotFoundError(
                f"Demo file not found: {self.path}. Run python scripts/generate_demo.py"
            )
        frame = pd.read_csv(self.path, parse_dates=["timestamp"])
        if start is not None:
            frame = frame[frame["timestamp"] >= pd.Timestamp(start)]
        if end is not None:
            frame = frame[frame["timestamp"] <= pd.Timestamp(end)]
        return frame.reset_index(drop=True)
