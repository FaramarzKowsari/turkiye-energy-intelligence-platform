# Data Card

## Dataset identity

**Name:** EnerjiNabız AI Synthetic Hourly Electricity Dataset
**Version:** 1.0.0
**Coverage:** 2,880 hourly rows covering 120 days
**License:** CC0 1.0
**Purpose:** Reproducible testing, teaching, software review and dashboard demonstration without account registration.

## Variables

The dataset includes timestamp, electricity consumption, total generation, market-clearing-price proxy and a generation mix covering gas, coal, hydro, wind, solar, geothermal and biomass. Provenance fields explicitly state `source=demo` and `is_synthetic=true`.

## Generation method

Values are created through deterministic seasonal functions, day-of-week effects, gradual trend, bounded random noise, renewable generation profiles and a small number of injected anomalies. A fixed random seed makes the dataset reproducible.

## Appropriate use

- Pipeline and schema testing
- Visualization development
- Forecasting demonstrations
- Anomaly-detection evaluation
- Power BI and Tableau import examples
- CI and release validation

## Inappropriate use

- Claims about actual Turkish demand, generation, price or carbon intensity
- Operational grid decisions
- Financial or trading decisions
- Benchmarking a production forecast without official holdout data
- Publication as an official government or market-operator dataset

## Known limitations

The synthetic process simplifies holidays, weather, plant outages, market constraints, cross-border flows and regulatory effects. Correlations are designed for demonstration and do not establish causal relationships.
