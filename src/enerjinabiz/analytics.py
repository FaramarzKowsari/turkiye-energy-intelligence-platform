from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


def add_features(frame: pd.DataFrame) -> pd.DataFrame:
    data = frame.copy().sort_values("timestamp")
    data["lag_1"] = data["consumption_mwh"].shift(1)
    data["lag_24"] = data["consumption_mwh"].shift(24)
    data["lag_168"] = data["consumption_mwh"].shift(168)
    data["rolling_24"] = data["consumption_mwh"].shift(1).rolling(24).mean()
    data["rolling_168"] = data["consumption_mwh"].shift(1).rolling(168).mean()
    data["hour_sin"] = np.sin(2 * np.pi * data["hour"] / 24)
    data["hour_cos"] = np.cos(2 * np.pi * data["hour"] / 24)
    data["dow"] = data["timestamp"].dt.dayofweek
    data["dow_sin"] = np.sin(2 * np.pi * data["dow"] / 7)
    data["dow_cos"] = np.cos(2 * np.pi * data["dow"] / 7)
    return data


def forecast_consumption(
    frame: pd.DataFrame,
    test_hours: int = 48,
) -> tuple[pd.DataFrame, dict]:
    data = add_features(frame).dropna(
        subset=["consumption_mwh", "lag_24", "rolling_24"]
    )
    if len(data) < test_hours + 72:
        raise ValueError("At least 120 clean hourly rows are required for forecasting")
    test_hours = min(test_hours, max(24, len(data) // 4))
    train = data.iloc[:-test_hours].copy()
    test = data.iloc[-test_hours:].copy()
    features = [
        "hour",
        "dow",
        "is_weekend",
        "lag_1",
        "lag_24",
        "rolling_24",
        "hour_sin",
        "hour_cos",
        "dow_sin",
        "dow_cos",
    ]
    if len(data) >= test_hours + 168 + 72:
        features.extend(["lag_168", "rolling_168"])
    features = [feature for feature in features if feature in data.columns]
    train = train.dropna(subset=features)
    test = test.dropna(subset=features)
    if len(train) < 72 or len(test) < 12:
        raise ValueError("Not enough complete hourly rows remain after feature engineering")

    model = RandomForestRegressor(
        n_estimators=180,
        max_depth=14,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(train[features], train["consumption_mwh"])
    test["forecast_mwh"] = model.predict(test[features])
    test["naive_24h_mwh"] = test["lag_24"]
    metrics = {
        "model": "RandomForestRegressor",
        "test_rows": int(len(test)),
        "mae": round(
            float(mean_absolute_error(test["consumption_mwh"], test["forecast_mwh"])),
            3,
        ),
        "rmse": round(
            float(
                mean_squared_error(test["consumption_mwh"], test["forecast_mwh"])
                ** 0.5
            ),
            3,
        ),
        "naive_mae": round(
            float(
                mean_absolute_error(
                    test["consumption_mwh"],
                    test["naive_24h_mwh"],
                )
            ),
            3,
        ),
    }
    columns = ["timestamp", "consumption_mwh", "forecast_mwh", "naive_24h_mwh"]
    return test[columns], metrics


def detect_anomalies(frame: pd.DataFrame) -> pd.DataFrame:
    data = frame.copy()
    candidates = [
        "consumption_mwh",
        "market_price_try_mwh",
        "renewable_share_pct",
    ]
    columns = [column for column in candidates if column in data]
    usable = data[columns].interpolate(limit_direction="both").dropna()
    data["anomaly_score"] = np.nan
    data["is_anomaly"] = False
    if len(usable) < 48:
        return data
    model = IsolationForest(contamination=0.025, random_state=42)
    labels = model.fit_predict(usable)
    scores = -model.score_samples(usable)
    data.loc[usable.index, "anomaly_score"] = scores
    data.loc[usable.index, "is_anomaly"] = labels == -1
    return data


def save_metrics(metrics: dict, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
