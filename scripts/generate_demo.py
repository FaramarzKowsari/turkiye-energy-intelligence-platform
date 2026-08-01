from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate(hours: int = 24 * 120, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    timestamps = pd.date_range("2026-04-01 00:00:00", periods=hours, freq="h")
    hour = timestamps.hour.to_numpy()
    dow = timestamps.dayofweek.to_numpy()
    day_index = np.arange(hours) / 24

    daily = 5500 * np.sin(2 * np.pi * (hour - 8) / 24)
    daily += 1800 * np.sin(4 * np.pi * (hour - 5) / 24)
    weekly = np.where(dow >= 5, -2500, 0)
    trend = 10 * day_index
    consumption = 34500 + daily + weekly + trend + rng.normal(0, 700, hours)

    solar_profile = np.maximum(0, 4500 * np.sin(np.pi * (hour - 6) / 12))
    solar = solar_profile * (0.82 + 0.16 * rng.random(hours))
    wind = 3800 + 1500 * np.sin(2 * np.pi * day_index / 6.5)
    wind += rng.normal(0, 500, hours)
    wind = np.maximum(800, wind)
    hydro = 7200 + 900 * np.sin(2 * np.pi * day_index / 28)
    hydro += rng.normal(0, 220, hours)
    runriver = 2500 + 400 * np.sin(2 * np.pi * day_index / 18)
    runriver += rng.normal(0, 120, hours)
    geothermal = np.full(hours, 1250.0) + rng.normal(0, 25, hours)
    biomass = np.full(hours, 950.0) + rng.normal(0, 30, hours)
    lignite = np.full(hours, 5200.0) + rng.normal(0, 260, hours)
    hardcoal = np.full(hours, 2800.0) + rng.normal(0, 180, hours)
    imported = np.full(hours, 6500.0) + rng.normal(0, 350, hours)
    base_non_gas = (
        solar
        + wind
        + hydro
        + runriver
        + geothermal
        + biomass
        + lignite
        + hardcoal
        + imported
    )
    gas = np.maximum(1500, consumption - base_non_gas + rng.normal(250, 180, hours))
    generation = base_non_gas + gas

    renewable = solar + wind + hydro + runriver + geothermal + biomass
    renewable_share = 100 * renewable / generation
    price = 1250 + 0.055 * consumption - 7.0 * renewable_share
    price += rng.normal(0, 90, hours)
    price = np.maximum(250, price)

    anomaly_indices = [420, 1020, 1660, 2150]
    for idx in anomaly_indices:
        if idx < hours:
            consumption[idx] *= 1.17
            price[idx] *= 1.32

    return pd.DataFrame(
        {
            "timestamp": timestamps,
            "consumption_mwh": consumption.round(2),
            "generation_mwh": generation.round(2),
            "market_price_try_mwh": price.round(2),
            "natural_gas_mwh": gas.round(2),
            "lignite_mwh": lignite.round(2),
            "hard_coal_mwh": hardcoal.round(2),
            "imported_coal_mwh": imported.round(2),
            "dam_hydro_mwh": hydro.round(2),
            "run_of_river_mwh": runriver.round(2),
            "wind_mwh": wind.round(2),
            "solar_mwh": solar.round(2),
            "geothermal_mwh": geothermal.round(2),
            "biomass_mwh": biomass.round(2),
            "source": "demo",
            "is_synthetic": True,
        }
    )


if __name__ == "__main__":
    target = Path("data/samples/energy_hourly_demo.csv")
    target.parent.mkdir(parents=True, exist_ok=True)
    frame = generate()
    frame.to_csv(target, index=False)

    docs_data = Path("docs/assets/demo-data.json")
    docs_data.parent.mkdir(parents=True, exist_ok=True)
    sample = frame.tail(24 * 14).copy()
    sample["timestamp"] = sample["timestamp"].astype(str)
    docs_data.write_text(sample.to_json(orient="records"), encoding="utf-8")
    print(f"Generated {len(frame)} demo rows at {target}")
