from __future__ import annotations

from pathlib import Path
from typing import Annotated

import pandas as pd
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    title="EnerjiNabız AI API",
    version="1.0.0",
    description="Read-only API over normalized Turkish electricity analytics data.",
)
DATA_PATH = Path("data/processed/energy_hourly.csv")


def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail="Processed data is unavailable. Run build scripts.",
        )
    return pd.read_csv(DATA_PATH, parse_dates=["timestamp"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "data_available": DATA_PATH.exists()}


@app.get("/kpis")
def kpis() -> dict:
    frame = load_data()
    return {
        "rows": len(frame),
        "start": frame["timestamp"].min(),
        "end": frame["timestamp"].max(),
        "average_consumption_mwh": frame["consumption_mwh"].mean(),
        "peak_consumption_mwh": frame["consumption_mwh"].max(),
        "average_price_try_mwh": frame["market_price_try_mwh"].mean(),
        "average_renewable_share_pct": frame["renewable_share_pct"].mean(),
    }


@app.get("/hourly")
def hourly(limit: Annotated[int, Query(ge=1, le=10000)] = 168) -> list[dict]:
    frame = load_data().tail(limit).copy()
    frame["timestamp"] = frame["timestamp"].astype(str)
    return frame.to_dict(orient="records")
