from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="EnerjiNabız AI", page_icon="⚡", layout="wide")

DATA = Path("data/processed/energy_hourly.csv")
FORECAST = Path("data/processed/consumption_forecast.csv")

st.title("EnerjiNabız AI")
st.caption("Türkiye Energy Intelligence Platform · Demo / local / optional EPİAŞ data")

if not DATA.exists():
    st.error(
        "Processed data is missing. Run `python scripts/generate_demo.py` "
        "and `python scripts/build_exports.py`."
    )
    st.stop()

frame = pd.read_csv(DATA, parse_dates=["timestamp"])

with st.sidebar:
    st.header("Filters")
    start, end = st.date_input(
        "Date range",
        value=(frame["timestamp"].min().date(), frame["timestamp"].max().date()),
    )
    metric = st.selectbox(
        "Primary metric",
        ["consumption_mwh", "market_price_try_mwh", "renewable_share_pct"],
    )

mask = (frame["timestamp"].dt.date >= start) & (frame["timestamp"].dt.date <= end)
data = frame.loc[mask].copy()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Average consumption", f"{data['consumption_mwh'].mean():,.0f} MWh")
c2.metric("Peak consumption", f"{data['consumption_mwh'].max():,.0f} MWh")
c3.metric("Average MCP", f"{data['market_price_try_mwh'].mean():,.0f} TRY/MWh")
c4.metric("Renewable share", f"{data['renewable_share_pct'].mean():.1f}%")

fig = px.line(data, x="timestamp", y=metric, title="Hourly trend")
st.plotly_chart(fig, use_container_width=True)

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
    if column in data
]
if generation_cols:
    daily = data.set_index("timestamp")[generation_cols].resample("D").sum().reset_index()
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
    st.plotly_chart(mix_chart, use_container_width=True)

heat = data.pivot_table(
    index="weekday",
    columns="hour",
    values="consumption_mwh",
    aggfunc="mean",
)
heat = heat.reindex(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)
heatmap = go.Figure(data=go.Heatmap(z=heat.values, x=heat.columns, y=heat.index))
heatmap.update_layout(title="Average consumption by weekday and hour")
st.plotly_chart(heatmap, use_container_width=True)

if "is_anomaly" in data:
    anomalies = data[data["is_anomaly"].astype(str).str.lower().isin(["true", "1"])]
    st.subheader("Detected anomalies")
    anomaly_columns = [
        "timestamp",
        "consumption_mwh",
        "market_price_try_mwh",
        "anomaly_score",
    ]
    st.dataframe(anomalies[anomaly_columns].tail(30), use_container_width=True)

if FORECAST.exists():
    forecast = pd.read_csv(FORECAST, parse_dates=["timestamp"])
    st.subheader("Forecast validation")
    forecast_chart = px.line(
        forecast,
        x="timestamp",
        y=["consumption_mwh", "forecast_mwh", "naive_24h_mwh"],
    )
    st.plotly_chart(forecast_chart, use_container_width=True)

st.info(
    "Demo data is synthetic and is clearly flagged. Enable EPİAŞ locally for "
    "official near-real-time records."
)
