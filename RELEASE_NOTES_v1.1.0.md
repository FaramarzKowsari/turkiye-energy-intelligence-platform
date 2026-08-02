# Türkiye Energy Intelligence Platform v1.1.0

## Live EPİAŞ Integration

Version 1.1.0 turns EnerjiNabız AI from a reproducible research demo into a hosted analytical application that can securely retrieve official EPİAŞ electricity-market data.

## Highlights

- Added a public Streamlit application:
  https://enerjinabiz-ai.streamlit.app
- Added a secure `Live EPİAŞ` mode using private Streamlit Secrets.
- Added authenticated retrieval of:
  - real-time electricity consumption,
  - real-time generation by energy source,
  - day-ahead Market Clearing Price (MCP / PTF).
- Added a switch between reproducible synthetic demo data and official EPİAŞ data.
- Added configurable live lookback windows from 1 to 14 days.
- Added manual refresh for official records.
- Added automatic fallback to demo data if the remote service is temporarily unavailable.
- Added data-quality indicators for coverage, missing timestamps and duplicate timestamps.
- Added filtered CSV export for the selected date range.
- Added source labels, latest-record timestamps and row counts to distinguish live and demo datasets.
- Updated Streamlit components to the current width API.
- Restored and retained the complete bilingual English/Turkish project README.

## Security and privacy

- EPİAŞ usernames and passwords are never stored in this repository.
- Hosted credentials are read only from Streamlit Community Cloud Secrets.
- No API secrets, session tickets, private datasets or user credentials are included in this release.
- Users who run the connector locally must keep credentials in an untracked `.env` file.

## Data statement

- The bundled demo dataset is synthetic and clearly labelled.
- Live mode requires each user or deployment owner to supply an authorized EPİAŞ account.
- Official EPİAŞ feeds may be published with an operational delay.
- This software is an analytical and educational system, not an official grid-control, emergency-warning or trading platform.

## Included analytical capabilities

- Hourly consumption and market-price trends
- Generation mix by source
- Renewable-energy share
- Weekday/hour heatmaps
- Forecast-validation views for demo data
- Anomaly tables when anomaly fields are available
- BI-ready CSV, Excel and optional Parquet workflows
- FastAPI and Streamlit application layers
- Bilingual GitHub Pages project website

## Reproducibility

Demo mode remains provider-independent and can be executed without registration:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev,app]"
python scripts/generate_demo.py
python scripts/build_exports.py
streamlit run app/streamlit_app.py
```

## Citation

All-versions / Concept DOI:

https://doi.org/10.5281/zenodo.21749628

The version-specific DOI for v1.1.0 will be added after Zenodo archives this GitHub release.
