import pandas as pd

from enerjinabiz.pipeline import clean_energy_data, quality_report


def test_clean_energy_data_builds_features():
    frame = pd.DataFrame(
        {
            "timestamp": ["2026-01-01 00:00", "2026-01-01 01:00"],
            "consumption_mwh": [100, 110],
            "generation_mwh": [105, 115],
            "market_price_try_mwh": [1000, 1100],
            "wind_mwh": [20, 25],
            "solar_mwh": [0, 0],
        }
    )
    result = clean_energy_data(frame)
    assert "renewable_share_pct" in result
    assert result.loc[0, "net_balance_mwh"] == 5
    assert result.loc[1, "hour"] == 1


def test_quality_report_detects_gap():
    frame = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2026-01-01 00:00", "2026-01-01 02:00"]),
            "consumption_mwh": [100, 120],
            "generation_mwh": [100, 120],
            "market_price_try_mwh": [900, 1000],
        }
    )
    clean = clean_energy_data(frame)
    report = quality_report(clean)
    assert report["missing_timestamp_count"] == 1
