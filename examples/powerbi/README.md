# Power BI integration

Run `python scripts/build_exports.py`, then import:

- `data/exports/fact_energy_hourly.csv`
- `data/exports/fact_generation_mix.csv`
- `data/exports/dim_datetime.csv`
- `data/exports/dashboard_kpis.csv`

Recommended relationships:

- `DimDateTime[timestamp]` → `FactEnergyHourly[timestamp]`
- `DimDateTime[timestamp]` → `FactGenerationMix[timestamp]`

Use the included Excel workbook for a single-file import. Do not connect Power BI directly to EPİAŞ credentials; let the Python layer handle authentication and normalization.
