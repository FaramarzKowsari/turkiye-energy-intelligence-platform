# Methodology

## Cleaning

- Parse timestamps and sort chronologically.
- Remove invalid timestamps and duplicate hourly records.
- Coerce numeric fields and null negative energy/price values.
- Reconstruct total generation from components when possible.
- Add time dimensions, renewable share and net balance.

## Quality

The report measures hourly coverage, missing timestamps, duplicates, missing values by field and the number of synthetic records.

## Forecasting

The reference model is a random forest using calendar variables, 1-hour, 24-hour and 168-hour lags, plus rolling means. It is compared with a 24-hour seasonal-naive baseline. This is a transparent engineering baseline, not a claim of market-leading accuracy.

## Anomaly detection

Isolation Forest identifies unusual combinations of consumption, price and renewable share. Flags should be investigated, not interpreted automatically as operational failures or market abuse.
