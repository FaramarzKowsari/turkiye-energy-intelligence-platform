from __future__ import annotations

from pathlib import Path

from enerjinabiz.analytics import detect_anomalies, forecast_consumption, save_metrics
from enerjinabiz.exports import build_bi_exports
from enerjinabiz.pipeline import clean_energy_data, quality_report, save_quality_report
from enerjinabiz.providers.demo import DemoProvider

if __name__ == "__main__":
    raw = DemoProvider().fetch()
    clean = detect_anomalies(clean_energy_data(raw))
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    clean.to_csv("data/processed/energy_hourly.csv", index=False)
    save_quality_report(quality_report(clean), "reports/data_quality_report.json")
    forecast, metrics = forecast_consumption(clean)
    forecast.to_csv("data/processed/consumption_forecast.csv", index=False)
    save_metrics(metrics, "reports/forecast_metrics.json")
    outputs = build_bi_exports(clean)
    print("Exports built:")
    for key, path in outputs.items():
        print(f"- {key}: {path}")
