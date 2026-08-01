from __future__ import annotations

from pathlib import Path

import typer

from enerjinabiz.analytics import detect_anomalies, forecast_consumption, save_metrics
from enerjinabiz.exports import build_bi_exports
from enerjinabiz.pipeline import clean_energy_data, quality_report, save_quality_report
from enerjinabiz.providers.factory import get_provider

app = typer.Typer(help="EnerjiNabız AI command line interface")


@app.command()
def build() -> None:
    provider = get_provider()
    raw = provider.fetch()
    clean = clean_energy_data(raw)
    clean = detect_anomalies(clean)
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    clean.to_csv("data/processed/energy_hourly.csv", index=False)
    save_quality_report(quality_report(clean), "reports/data_quality_report.json")
    forecast, metrics = forecast_consumption(clean)
    forecast.to_csv("data/processed/consumption_forecast.csv", index=False)
    save_metrics(metrics, "reports/forecast_metrics.json")
    build_bi_exports(clean)
    typer.echo(f"Built {len(clean)} hourly rows from provider={provider.name}")


@app.command()
def catalog() -> None:
    from enerjinabiz.providers.teias import TeiasCatalogProvider

    frame = TeiasCatalogProvider().fetch()
    typer.echo(frame.to_string(index=False))


if __name__ == "__main__":
    app()
