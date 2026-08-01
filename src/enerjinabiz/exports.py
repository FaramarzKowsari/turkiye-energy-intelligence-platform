from __future__ import annotations

from pathlib import Path

import pandas as pd

GENERATION_MAP = {
    "natural_gas_mwh": "Natural gas",
    "lignite_mwh": "Lignite",
    "hard_coal_mwh": "Hard coal",
    "imported_coal_mwh": "Imported coal",
    "dam_hydro_mwh": "Dam hydro",
    "run_of_river_mwh": "Run-of-river",
    "wind_mwh": "Wind",
    "solar_mwh": "Solar",
    "geothermal_mwh": "Geothermal",
    "biomass_mwh": "Biomass",
}


def build_bi_exports(
    frame: pd.DataFrame,
    output_dir: str | Path = "data/exports",
) -> dict[str, Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    fact_cols = [
        "timestamp",
        "date",
        "year",
        "month",
        "day",
        "hour",
        "weekday",
        "is_weekend",
        "consumption_mwh",
        "generation_mwh",
        "market_price_try_mwh",
        "net_balance_mwh",
        "renewable_generation_mwh",
        "renewable_share_pct",
        "source",
        "is_synthetic",
    ]
    fact = frame[[column for column in fact_cols if column in frame]].copy()
    fact_path = out / "fact_energy_hourly.csv"
    fact.to_csv(fact_path, index=False)

    generation_cols = [column for column in GENERATION_MAP if column in frame]
    mix = frame[["timestamp", *generation_cols]].melt(
        id_vars="timestamp",
        var_name="source_key",
        value_name="generation_mwh",
    )
    mix["generation_source"] = mix["source_key"].map(GENERATION_MAP)
    mix = mix.drop(columns="source_key")
    mix_path = out / "fact_generation_mix.csv"
    mix.to_csv(mix_path, index=False)

    dimension_cols = [
        "timestamp",
        "date",
        "year",
        "month",
        "day",
        "hour",
        "weekday",
        "is_weekend",
    ]
    dimension = frame[dimension_cols].drop_duplicates()
    dim_path = out / "dim_datetime.csv"
    dimension.to_csv(dim_path, index=False)

    kpis = pd.DataFrame(
        {
            "metric": [
                "Average consumption (MWh)",
                "Peak consumption (MWh)",
                "Average market price (TRY/MWh)",
                "Average renewable share (%)",
                "Hourly records",
            ],
            "value": [
                frame["consumption_mwh"].mean(),
                frame["consumption_mwh"].max(),
                frame["market_price_try_mwh"].mean(),
                frame["renewable_share_pct"].mean(),
                len(frame),
            ],
        }
    )
    kpi_path = out / "dashboard_kpis.csv"
    kpis.to_csv(kpi_path, index=False)

    workbook_path = out / "enerjinabiz_bi_pack.xlsx"
    with pd.ExcelWriter(workbook_path, engine="openpyxl") as writer:
        fact.to_excel(writer, sheet_name="FactEnergyHourly", index=False)
        mix.to_excel(writer, sheet_name="FactGenerationMix", index=False)
        dimension.to_excel(writer, sheet_name="DimDateTime", index=False)
        kpis.to_excel(writer, sheet_name="DashboardKPIs", index=False)

    parquet_path = out / "fact_energy_hourly.parquet"
    try:
        fact.to_parquet(parquet_path, index=False)
    except ImportError:
        parquet_path = Path("PyArrow not installed")

    return {
        "fact": fact_path,
        "mix": mix_path,
        "datetime": dim_path,
        "kpis": kpi_path,
        "workbook": workbook_path,
        "parquet": parquet_path,
    }
