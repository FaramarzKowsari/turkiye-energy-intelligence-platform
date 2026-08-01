from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

import pandas as pd


class EnergyDataProvider(ABC):
    """Provider contract returning a normalized wide hourly dataframe."""

    name: str

    @abstractmethod
    def fetch(self, start: datetime | None = None, end: datetime | None = None) -> pd.DataFrame:
        raise NotImplementedError
