from pathlib import Path

import pandas as pd

from enerjinabiz.exports import build_bi_exports
from enerjinabiz.pipeline import clean_energy_data


def test_build_bi_exports(tmp_path: Path):
    frame = clean_energy_data(
        pd.DataFrame(
            {
                "timestamp": pd.date_range("2026-01-01", periods=4, freq="h"),
                "consumption_mwh": [100, 110, 120, 130],
                "generation_mwh": [101, 111, 121, 131],
                "market_price_try_mwh": [900, 920, 940, 960],
                "wind_mwh": [10, 12, 14, 15],
                "solar_mwh": [0, 0, 1, 2],
            }
        )
    )
    outputs = build_bi_exports(frame, tmp_path)
    assert outputs["fact"].exists()
    assert outputs["workbook"].exists()
