from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = [
    "timestamp",
    "consumption_mwh",
    "generation_mwh",
    "market_price_try_mwh",
]
GENERATION_COLUMNS = [
    "natural_gas_mwh",
    "lignite_mwh",
    "hard_coal_mwh",
    "imported_coal_mwh",
    "dam_hydro_mwh",
    "run_of_river_mwh",
    "wind_mwh",
    "solar_mwh",
    "geothermal_mwh",
    "biomass_mwh",
]
RENEWABLE_COLUMNS = [
    "dam_hydro_mwh",
    "run_of_river_mwh",
    "wind_mwh",
    "solar_mwh",
    "geothermal_mwh",
    "biomass_mwh",
]


def clean_energy_data(frame: pd.DataFrame) -> pd.DataFrame:
    data = frame.copy()
    if "timestamp" not in data:
        raise ValueError("timestamp column is required")
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    data = data.dropna(subset=["timestamp"]).sort_values("timestamp")
    data = data.drop_duplicates(subset=["timestamp"], keep="last")

    candidates = REQUIRED_COLUMNS[1:] + GENERATION_COLUMNS
    numeric_candidates = [column for column in candidates if column in data]
    for column in numeric_candidates:
        data[column] = pd.to_numeric(data[column], errors="coerce")
        data.loc[data[column] < 0, column] = np.nan

    for column in REQUIRED_COLUMNS[1:]:
        if column not in data:
            data[column] = np.nan

    if data["generation_mwh"].isna().all():
        available = [column for column in GENERATION_COLUMNS if column in data]
        if available:
            data["generation_mwh"] = data[available].sum(axis=1, min_count=1)

    data["date"] = data["timestamp"].dt.date.astype(str)
    data["year"] = data["timestamp"].dt.year
    data["month"] = data["timestamp"].dt.month
    data["day"] = data["timestamp"].dt.day
    data["hour"] = data["timestamp"].dt.hour
    data["weekday"] = data["timestamp"].dt.day_name()
    data["is_weekend"] = data["timestamp"].dt.dayofweek >= 5
    data["net_balance_mwh"] = data["generation_mwh"] - data["consumption_mwh"]

    renewable = [column for column in RENEWABLE_COLUMNS if column in data]
    if renewable:
        data["renewable_generation_mwh"] = data[renewable].sum(
            axis=1,
            min_count=1,
        )
    else:
        data["renewable_generation_mwh"] = np.nan
    data["renewable_share_pct"] = (
        100
        * data["renewable_generation_mwh"]
        / data["generation_mwh"].replace(0, np.nan)
    )
    data["source"] = data.get("source", "unknown")
    data["is_synthetic"] = data.get("is_synthetic", False)
    return data.reset_index(drop=True)


def quality_report(frame: pd.DataFrame) -> dict:
    if frame.empty or "timestamp" not in frame:
        return {
            "rows": 0,
            "coverage_pct": 0.0,
            "missing_timestamp_count": 0,
            "duplicate_timestamp_count": 0,
            "missing_by_column": {},
            "synthetic_rows": 0,
        }
    expected = pd.date_range(
        frame["timestamp"].min(),
        frame["timestamp"].max(),
        freq="h",
    )
    missing_timestamps = expected.difference(pd.DatetimeIndex(frame["timestamp"]))
    missing_by_column = {
        column: int(frame[column].isna().sum()) for column in frame.columns
    }
    duplicate_count = int(frame.duplicated(subset=["timestamp"]).sum())
    coverage = (
        0.0
        if len(expected) == 0
        else round(min(100.0, 100 * len(frame) / len(expected)), 2)
    )
    synthetic = frame.get("is_synthetic", pd.Series(False, index=frame.index))
    return {
        "rows": int(len(frame)),
        "start": frame["timestamp"].min().isoformat(),
        "end": frame["timestamp"].max().isoformat(),
        "expected_hourly_rows": int(len(expected)),
        "coverage_pct": coverage,
        "missing_timestamp_count": int(len(missing_timestamps)),
        "duplicate_timestamp_count": duplicate_count,
        "missing_by_column": missing_by_column,
        "synthetic_rows": int(synthetic.sum()),
    }


def save_quality_report(report: dict, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
