# Data dictionary

| Column | Type | Meaning |
|---|---|---|
| `timestamp` | datetime | Hourly observation time |
| `consumption_mwh` | float | Electricity consumption |
| `generation_mwh` | float | Total electricity generation |
| `market_price_try_mwh` | float | Day-ahead market clearing price |
| `natural_gas_mwh` | float | Natural-gas generation |
| `lignite_mwh` | float | Lignite generation |
| `hard_coal_mwh` | float | Hard-coal generation |
| `imported_coal_mwh` | float | Imported-coal generation |
| `dam_hydro_mwh` | float | Reservoir hydropower generation |
| `run_of_river_mwh` | float | Run-of-river hydropower generation |
| `wind_mwh` | float | Wind generation |
| `solar_mwh` | float | Solar generation |
| `geothermal_mwh` | float | Geothermal generation |
| `biomass_mwh` | float | Biomass generation |
| `renewable_share_pct` | float | Renewable generation divided by total generation |
| `net_balance_mwh` | float | Generation minus consumption |
| `source` | string | Provider identifier |
| `is_synthetic` | boolean | Whether the record is simulated |
