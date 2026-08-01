# Data sources and access modes

## EPİAŞ Transparency Platform

Optional authenticated connector. The implementation follows the official electrical-services documentation for TGT creation and three endpoints:

- `/v1/consumption/data/realtime-consumption`
- `/v1/generation/data/realtime-generation`
- `/v1/markets/dam/data/mcp`

The platform's own documentation should be treated as the source of truth. Endpoint behavior, schemas and access policies can change.

## TEİAŞ public reports

TEİAŞ publishes sector and monthly electricity production-consumption reports. Because individual file formats can vary, the repository's public connector discovers report links instead of assuming one permanent spreadsheet schema.

## Demo data

The bundled demo dataset is synthetic, deterministic and explicitly marked with `is_synthetic=true`. It supports reproducible tests, screenshots and offline demonstrations. It must not be presented as measured Turkish market data.

## Local files

Users may bring their own CSV, XLSX or Parquet file. At minimum it must contain a `timestamp` column. The preferred canonical columns are documented in `docs/DATA_DICTIONARY.md`.
