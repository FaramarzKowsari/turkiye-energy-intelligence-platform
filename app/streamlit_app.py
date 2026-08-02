from __future__ import annotations

import importlib
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

EpiasProvider = importlib.import_module(
    "enerjinabiz.providers.epias"
).EpiasProvider
pipeline_module = importlib.import_module("enerjinabiz.pipeline")
clean_energy_data = pipeline_module.clean_energy_data
quality_report = pipeline_module.quality_report

st.set_page_config(page_title="EnerjiNabız AI", page_icon="⚡", layout="wide")

DATA = ROOT / "data/processed/energy_hourly.csv"
FORECAST = ROOT / "data/processed/consumption_forecast.csv"
DEFAULT_BASE_URL = "https://seffaflik.epias.com.tr/electricity-service"
DEFAULT_AUTH_URL = "https://giris.epias.com.tr/cas/v1/tickets"


def get_secret(name: str, default: str | None = None) -> str | None:
    """Read an EPİAŞ value from Streamlit Secrets without exposing it."""
    try:
        epias = st.secrets.get("epias", {})
        value = epias.get(name)
        if value:
            return str(value)
        top_level = st.secrets.get(f"EPIAS_{name.upper()}")
        if top_level:
            return str(top_level)
    except Exception:
        return default
    return default


@st.cache_data(show_spinner=False)
def load_demo() -> pd.DataFrame:
    if not DATA.exists():
        raise FileNotFoundError(
            "Processed demo data is missing. Run scripts/generate_demo.py and "
            "scripts/build_exports.py."
        )
    return clean_energy_data(pd.read_csv(DATA, parse_dates=["timestamp"]))


def load_live(lookback_days: int, refresh: bool) -> pd.DataFrame:
    """Fetch official data once per session unless a refresh is requested."""
    username = get_secret("username")
    password = get_secret("password")
    if not username or not password:
        raise RuntimeError("EPİAŞ Streamlit Secrets are not configured.")

    cache_key = f"epias-{lookback_days}"
    if refresh or st.session_state.get("epias_cache_key") != cache_key:
        end = datetime.now() - timedelta(hours=3)
        start = end - timedelta(days=lookback_days)
        provider = EpiasProvider(
            username=username,
            password=password,
            base_url=get_secret("base_url", DEFAULT_BASE_URL) or DEFAULT_BASE_URL,
            auth_url=get_secret("auth_url", DEFAULT_AUTH_URL) or DEFAULT_AUTH_URL,
        )
        with st.spinner("Fetching official EPİAŞ records..."):
            live_frame = clean_energy_data(provider.fetch(start=start, end=end))
        st.session_state["epias_frame"] = live_frame
        st.session_state["epias_cache_key"] = cache_key
        st.session_state["epias_fetched_at"] = datetime.now().isoformat(
            timespec="seconds"
        )
    return st.session_state["epias_frame"].copy()


def formatted_metric(data: pd.DataFrame, column: str, suffix: str) -> str:
    if column not in data or data[column].dropna().empty:
        return "N/A"
    return f"{data[column].mean():,.1f}{suffix}"


def peak_metric(data: pd.DataFrame, column: str, suffix: str) -> str:
    if column not in data or data[column].dropna().empty:
        return "N/A"
    return f"{data[column].max():,.0f}{suffix}"


st.title("EnerjiNabız AI")
st.caption(
    "Türkiye Energy Intelligence Platform · reproducible demo or official "
    "EPİAŞ data"
)

username_configured = bool(get_secret("username"))
password_configured = bool(get_secret("password"))
live_available = username_configured and password_configured

with st.sidebar:
    st.header("Data source")
    source_options = ["Demo data"]
    if live_available:
        source_options.append("Live EPİAŞ")
    selected_source = st.radio("Mode", source_options)

    lookback_days = 7
    refresh_live = False
    if selected_source == "Live EPİAŞ":
        lookback_days = st.slider("Live lookback (days)", 1, 14, 7)
        refresh_live = st.button("Refresh official data", width="stretch")
        st.caption("Credentials are stored only in Streamlit Secrets.")
    else:
        st.caption("Synthetic data is clearly labelled and requires no account.")
        if not live_available:
            st.info(
                "Live mode appears after the app owner configures the EPİAŞ "
                "username and password in Streamlit Secrets."
            )

try:
    if selected_source == "Live EPİAŞ":
        frame = load_live(lookback_days, refresh_live)
        source_label = "Official EPİAŞ"
    else:
        frame = load_demo()
        source_label = "Synthetic demo"
except Exception as exc:
    st.error(f"Could not load {selected_source}: {exc}")
    if selected_source == "Live EPİAŞ":
        st.warning("Falling back to the reproducible demo dataset.")
        frame = load_demo()
        selected_source = "Demo data"
        source_label = "Synthetic demo"
    else:
        st.stop()

if frame.empty:
    st.error("The selected source returned no usable hourly records.")
    st.stop()

report: dict[str, Any] = quality_report(frame)

with st.sidebar:
    st.header("Filters")
    min_date = frame["timestamp"].min().date()
    max_date = frame["timestamp"].max().date()
    date_value = st.date_input("Date range", value=(min_date, max_date))
    if isinstance(date_value, tuple) and len(date_value) == 2:
        start, end = date_value
    else:
        start, end = min_date, max_date

    metric_candidates = [
        column
        for column in [
            "consumption_mwh",
            "market_price_try_mwh",
            "renewable_share_pct",
            "generation_mwh",
        ]
        if column in frame and not frame[column].dropna().empty
    ]
    metric = st.selectbox("Primary metric", metric_candidates)

mask = (frame["timestamp"].dt.date >= start) & (
    frame["timestamp"].dt.date <= end
)
data = frame.loc[mask].copy()
if data.empty:
    st.warning("No records are available in the selected date range.")
    st.stop()

if selected_source == "Live EPİAŞ":
    latest = data["timestamp"].max().strftime("%Y-%m-%d %H:%M")
    st.success(
        f"Source: {source_label} · latest record: {latest} Europe/Istanbul · "
        f"{len(data):,} hourly rows"
    )
else:
    st.warning(
        f"Source: {source_label} · {len(data):,} hourly rows · not for "
        "operational decisions"
    )

c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "Average consumption",
    formatted_metric(data, "consumption_mwh", " MWh"),
)
c2.metric(
    "Peak consumption",
    peak_metric(data, "consumption_mwh", " MWh"),
)
c3.metric(
    "Average MCP",
    formatted_metric(data, "market_price_try_mwh", " TRY/MWh"),
)
c4.metric(
    "Renewable share",
    formatted_metric(data, "renewable_share_pct", "%"),
)

fig = px.line(data, x="timestamp", y=metric, title="Hourly trend")
st.plotly_chart(fig, width="stretch")

generation_cols = [
    column
    for column in [
        "natural_gas_mwh",
        "lignite_mwh",
        "hard_coal_mwh",
        "imported_coal_mwh",
        "dam_hydro_mwh",
        "run_of_river_mwh",
        "wind_mwh",
        "solar_mwh",
        "geothermal_mwh",
        "biomass_mwh",
    ]
    if column in data and not data[column].dropna().empty
]
if generation_cols:
    daily = (
        data.set_index("timestamp")[generation_cols]
        .resample("D")
        .sum()
        .reset_index()
    )
    mix = daily.melt(
        id_vars="timestamp",
        var_name="source",
        value_name="generation_mwh",
    )
    mix_chart = px.area(
        mix,
        x="timestamp",
        y="generation_mwh",
        color="source",
        title="Daily generation mix",
    )
    st.plotly_chart(mix_chart, width="stretch")

if "consumption_mwh" in data and not data["consumption_mwh"].dropna().empty:
    heat = data.pivot_table(
        index="weekday",
        columns="hour",
        values="consumption_mwh",
        aggfunc="mean",
    )
    heat = heat.reindex(
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
    )
    heatmap = go.Figure(
        data=go.Heatmap(z=heat.values, x=heat.columns, y=heat.index)
    )
    heatmap.update_layout(title="Average consumption by weekday and hour")
    st.plotly_chart(heatmap, width="stretch")

if "is_anomaly" in data:
    anomalies = data[
        data["is_anomaly"].astype(str).str.lower().isin(["true", "1"])
    ]
    if not anomalies.empty:
        st.subheader("Detected anomalies")
        anomaly_columns = [
            column
            for column in [
                "timestamp",
                "consumption_mwh",
                "market_price_try_mwh",
                "anomaly_score",
            ]
            if column in anomalies
        ]
        st.dataframe(
            anomalies[anomaly_columns].tail(30),
            width="stretch",
        )

if selected_source == "Demo data" and FORECAST.exists():
    forecast = pd.read_csv(FORECAST, parse_dates=["timestamp"])
    st.subheader("Forecast validation")
    forecast_chart = px.line(
        forecast,
        x="timestamp",
        y=["consumption_mwh", "forecast_mwh", "naive_24h_mwh"],
    )
    st.plotly_chart(forecast_chart, width="stretch")

st.subheader("Data quality and export")
q1, q2, q3 = st.columns(3)
q1.metric("Coverage", f"{report.get('coverage_pct', 0):.1f}%")
q2.metric("Missing timestamps", f"{report.get('missing_timestamp_count', 0):,}")
q3.metric("Duplicate timestamps", f"{report.get('duplicate_timestamp_count', 0):,}")
file_label = "live-epias" if selected_source == "Live EPİAŞ" else "demo"
st.download_button(
    "Download filtered CSV",
    data.to_csv(index=False).encode("utf-8"),
    file_name=f"enerjinabiz-{file_label}.csv",
    mime="text/csv",
)

if selected_source == "Live EPİAŞ":
    st.info(
        "EPİAŞ real-time consumption is officially published with a delay. "
        "This dashboard is analytical and is not an official grid-control or "
        "trading system."
    )
else:
    st.info(
        "Demo data is synthetic and clearly flagged. Live mode becomes "
        "available only after secure Streamlit Secrets are configured."
    )
