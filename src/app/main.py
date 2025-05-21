import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import xarray as xr

# ---------- Configuration ----------
st.set_page_config(layout="wide")
st.title("🌊 Climate Monitoring Dashboard")


# ---------- Load Dataset ----------
@st.cache_data
def load_data():
    # For prototyping: simulate a dataset
    times = pd.date_range("2023-01-01", periods=100, freq="D")
    lats = [58.0, 59.0, 60.0, 61.0]
    lons = [5.0, 6.0, 7.0, 8.0]
    temperature = np.random.rand(len(times), len(lats), len(lons)) * 10 + 5
    sea_level = np.random.rand(len(times), len(lats), len(lons)) * 0.5 + 0.5

    ds = xr.Dataset(
        {
            "temperature": (["time", "lat", "lon"], temperature),
            "sea_level": (["time", "lat", "lon"], sea_level),
        },
        coords={"time": times, "lat": lats, "lon": lons},
    )
    return ds


ds = load_data()

# ---------- Time Selection ----------
st.sidebar.header("🕒 Time Control")
time_options = pd.to_datetime(ds.time.values).to_pydatetime()
selected_time = st.sidebar.slider(
    "Select Time",
    min_value=time_options[0],
    max_value=time_options[-1],
    value=time_options[0],
    format="YYYY-MM-DD",
)


# ---------- User Thresholds ----------
st.sidebar.header("🚨 Alarm Thresholds")
temp_thresh = st.sidebar.slider("Temperature Threshold (°C)", 0.0, 20.0, 12.0)
sea_thresh = st.sidebar.slider("Sea Level Threshold (m)", 0.0, 2.0, 1.0)

# ---------- Select Locations ----------
locations = {
    "Site A": (58.0, 5.0),
    "Site B": (59.0, 6.0),
    "Site C": (60.0, 7.0),
    "Site D": (61.0, 8.0),
}

# ---------- Layout ----------
col1, col2 = st.columns([1.2, 2])

# ---------- Map View (col1) ----------
with col1:
    st.subheader(f"🗺️ Map Overview ({selected_time.date()})")
    # Select temperature data for chosen time
    temp_sel = (
        ds.temperature.sel(time=selected_time, method="nearest")
        .to_dataframe()
        .reset_index()
    )

    fig_map = px.density_mapbox(
        temp_sel,
        lat="lat",
        lon="lon",
        z="temperature",
        radius=30,
        center=dict(lat=59.5, lon=6.5),
        zoom=4,
        mapbox_style="carto-positron",
        title="Surface Temperature Snapshot",
    )
    st.plotly_chart(fig_map, use_container_width=True)

# ---------- Time Series (col2) ----------
with col2:
    st.subheader("📈 Time Series for Key Locations")
    fig_ts, axs = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

    alarm_triggered = False

    for i, (site, (lat, lon)) in enumerate(locations.items()):
        ts_temp = ds.temperature.sel(lat=lat, lon=lon, method="nearest").to_series()
        ts_sea = ds.sea_level.sel(lat=lat, lon=lon, method="nearest").to_series()

        axs[i].plot(
            ts_temp.index, ts_temp.values, label="Temperature (°C)", color="red"
        )
        axs[i].plot(ts_sea.index, ts_sea.values, label="Sea Level (m)", color="blue")
        axs[i].set_title(f"{site}")
        axs[i].legend(loc="upper right")
        axs[i].grid(True)

        # Alarm check
        if (ts_temp > temp_thresh).any() or (ts_sea > sea_thresh).any():
            alarm_triggered = True

    st.pyplot(fig_ts)

    # ---------- Alarm ----------
    if alarm_triggered:
        st.error("🚨 Alarm: One or more thresholds exceeded!")
    else:
        st.success("✅ All values within safe thresholds.")
