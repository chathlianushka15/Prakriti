import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

st.set_page_config(page_title="Prakriti", page_icon="🌿", layout="wide")

st.markdown("""
<style>
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #f0f0f0;
    }

    /* Cards */
    .metric-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    .metric-city {
        font-size: 13px;
        color: #a0b4c0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
    }
    .metric-temp {
        font-size: 36px;
        font-weight: 700;
        color: #ffffff;
    }
    .metric-aqi {
        font-size: 13px;
        color: #7ecba1;
        margin-top: 6px;
    }

    /* Section headers */
    .section-title {
        font-size: 14px;
        font-weight: 600;
        color: #a0b4c0;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 32px 0 16px 0;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Chart backgrounds */
    .stPlotlyChart, [data-testid="stArrowVegaLiteChart"] {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 12px;
        padding: 12px;
    }

    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.08);
    }

    /* Dataframe */
    .stDataFrame {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style='padding: 40px 0 20px 0'>
    <div style='font-size:11px; color:#7ecba1; letter-spacing:3px; text-transform:uppercase; margin-bottom:8px'>Environmental Intelligence</div>
    <div style='font-size:40px; font-weight:800; color:#ffffff; letter-spacing:-1px'>Prakriti</div>
    <div style='font-size:14px; color:#a0b4c0; margin-top:6px'>Real-time monitoring across Chandigarh & Haryana</div>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_weather():
    return pd.read_sql("SELECT * FROM weather ORDER BY timestamp DESC", engine)

@st.cache_data(ttl=3600)
def load_airquality():
    return pd.read_sql("SELECT * FROM airquality ORDER BY timestamp DESC", engine)

weather_df = load_weather()
aqi_df = load_airquality()

latest_weather = weather_df.drop_duplicates(subset="city", keep="first")
latest_aqi = aqi_df.drop_duplicates(subset="city", keep="first")

st.markdown('<div class="section-title">Current Conditions</div>', unsafe_allow_html=True)
cols = st.columns(5)
cities = latest_weather.to_dict("records")

for i, row in enumerate(cities):
    city_aqi = latest_aqi[latest_aqi["city"] == row["city"]]["aqi_value"].values
    aqi_val = round(city_aqi[0], 2) if len(city_aqi) > 0 else "N/A"
    with cols[i]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-city">{row['city']}</div>
            <div class="metric-temp">{row['temperature']}°</div>
            <div style="font-size:12px; color:#a0b4c0; margin-top:4px">{row['weather'].title()}</div>
            <div class="metric-aqi">AQI {aqi_val}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.divider()


col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-title">Temperature (°C)</div>', unsafe_allow_html=True)
    st.bar_chart(latest_weather.set_index("city")["temperature"], color="#4ecdc4")

with col2:
    st.markdown('<div class="section-title">Humidity (%)</div>', unsafe_allow_html=True)
    st.bar_chart(latest_weather.set_index("city")["humidity"], color="#45b7d1")

st.markdown('<div class="section-title">Air Quality Index</div>', unsafe_allow_html=True)
st.bar_chart(latest_aqi.set_index("city")["aqi_value"], color="#7ecba1")

st.divider()


with st.expander("View Raw Weather Data"):
    st.dataframe(weather_df, use_container_width=True)

with st.expander("View Raw Air Quality Data"):
    st.dataframe(aqi_df, use_container_width=True)

st.markdown("""
<div style='text-align:center; color:#4a6070; font-size:12px; padding:32px 0 16px 0'>
    Data refreshes every hour &nbsp;|&nbsp; OpenWeatherMap + OpenAQ (HSPCB) &nbsp;|&nbsp; Prakriti Environmental Pipeline
</div>
""", unsafe_allow_html=True)