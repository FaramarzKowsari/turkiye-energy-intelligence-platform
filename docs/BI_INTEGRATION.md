# Power BI and Tableau integration

## Recommended files

- `fact_energy_hourly.csv`
- `fact_generation_mix.csv`
- `dim_datetime.csv`
- `dashboard_kpis.csv`
- `enerjinabiz_bi_pack.xlsx`

## Model

Create one-to-many relationships from `DimDateTime[timestamp]` to each fact table. Use `generation_source` as the categorical field for stacked generation charts.

## Refresh strategy

Do not connect Power BI or Tableau directly to EPİAŞ credentials. Run the Python ingestion layer first, write normalized files or database tables, then refresh the BI model from those outputs. This isolates authentication, retries, schema drift and quality controls from the visualization layer.
