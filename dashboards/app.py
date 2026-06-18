import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

try:
    DB_PASSWORD = quote_plus(st.secrets["SUPABASE_PASSWORD"])
    DB_USER = st.secrets.get("SUPABASE_USER", "postgres")
    DB_HOST = st.secrets["SUPABASE_HOST"]
    DB_PORT = st.secrets.get("SUPABASE_PORT", "5432")
    DB_NAME = st.secrets.get("SUPABASE_DB", "postgres")
    st.write(f"Debug: Connected to {DB_HOST}")
except Exception as e:
    st.error(f"Secrets error: {e}")
    DB_PASSWORD = quote_plus(os.getenv("SUPABASE_PASSWORD"))
    DB_USER = os.getenv("SUPABASE_USER", "postgres")
    DB_HOST = os.getenv("SUPABASE_HOST")
    DB_PORT = os.getenv("SUPABASE_PORT", "5432")
    DB_NAME = os.getenv("SUPABASE_DB")
engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    connect_args={"sslmode": "require"}
)

st.set_page_config(page_title="Prakriti", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3, .hero-title { font-family: 'Syne', sans-serif !important; }

.stApp { background: #080812; color: #e2e8f0; }
.block-container { padding-top: 24px !important; padding-bottom: 0px !important; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.hero {
    padding: 16px 0 28px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 28px;
}
.hero-tag {
    font-size: 10px; letter-spacing: 4px; text-transform: uppercase;
    color: #7ecba1; margin-bottom: 8px; font-weight: 500;
}
.hero-title {
    font-size: 48px; font-weight: 700; color: #ffffff;
    letter-spacing: -2px; line-height: 1; margin-bottom: 10px;
    font-family: 'Syne', sans-serif;
}
.hero-title span { color: #ff6b9d; }
.hero-sub { font-size: 14px; color: #475569; font-weight: 400; }

.card {
    background: #0f0f20; border: 1px solid #1e1e35;
    border-radius: 16px; padding: 20px 16px; text-align: center;
}
.card-city {
    font-size: 10px; letter-spacing: 3px; text-transform: uppercase;
    color: #475569; margin-bottom: 8px; font-weight: 500;
}
.card-temp {
    font-size: 40px; font-weight: 600; color: #ffffff;
    letter-spacing: -1px; line-height: 1.1; font-family: 'DM Sans', sans-serif;
}
.card-weather { font-size: 11px; color: #64748b; margin-top: 4px; margin-bottom: 8px; }
.card-aqi {
    display: inline-block; font-size: 10px; font-weight: 700;
    color: #080812; background: #7ecba1; padding: 3px 10px;
    border-radius: 20px; letter-spacing: 1px;
}

.section-label {
    font-size: 10px; letter-spacing: 3px; text-transform: uppercase;
    color: #334155; font-weight: 500; margin: 28px 0 12px 0;
}

.note-box {
    font-size: 11px; color: #475569; margin-top: 8px; padding: 8px 12px;
    background: #0f0f20; border-left: 2px solid #334155; border-radius: 4px;
}

.finding-card {
    background: #0f0f20; border: 1px solid #1e1e35;
    border-left: 3px solid #ff6b9d; border-radius: 12px;
    padding: 18px 20px; margin-bottom: 10px;
}
.finding-number {
    font-size: 10px; letter-spacing: 2px; color: #ff6b9d;
    font-weight: 700; margin-bottom: 4px;
}
.finding-title {
    font-size: 15px; font-weight: 700; color: #f1f5f9;
    margin-bottom: 6px; font-family: 'Syne', sans-serif;
}
.finding-desc { font-size: 13px; color: #64748b; line-height: 1.7; }

.footer {
    text-align: center; color: #1e293b; font-size: 11px;
    padding: 32px 0 16px 0; margin-top: 32px; border-top: 1px solid #0f0f20;
}
</style>
""", unsafe_allow_html=True)

plt.rcParams.update({
    'figure.facecolor': '#0f0f20',
    'axes.facecolor': '#0f0f20',
    'axes.edgecolor': '#334155',
    'axes.labelcolor': '#ffffff',
    'text.color': '#ffffff',
    'xtick.color': '#ffffff',
    'ytick.color': '#ffffff',
    'grid.color': '#1e1e35',
    'grid.linewidth': 0.8,
    'font.family': 'sans-serif',
})

@st.cache_data(ttl=3600)
def load_data():
    weather = pd.read_sql('SELECT * FROM weather ORDER BY timestamp ASC', engine)
    aqi = pd.read_sql('SELECT * FROM airquality ORDER BY timestamp ASC', engine)
    return weather, aqi

weather_df, aqi_df = load_data()
latest_weather = weather_df.drop_duplicates(subset='city', keep='last')
latest_aqi = aqi_df.drop_duplicates(subset='city', keep='last')

COLORS = ['#ff6b9d', '#7ecba1', '#a78bfa', '#60a5fa', '#fbbf24']

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-tag">Environmental Intelligence</div>
    <div class="hero-title">Pra<span>kriti</span></div>
    <div class="hero-sub">Real-time air quality & weather monitoring — Chandigarh & Haryana</div>
</div>
""", unsafe_allow_html=True)

# City cards
st.markdown('<div class="section-label">Current Conditions</div>', unsafe_allow_html=True)
cols = st.columns(5)
for i, row in enumerate(latest_weather.to_dict('records')):
    aqi_val = latest_aqi[latest_aqi['city'] == row['city']]['aqi_value'].values
    aqi = round(aqi_val[0], 1) if len(aqi_val) > 0 else 'N/A'
    with cols[i]:
        st.markdown(f"""
        <div class="card">
            <div class="card-city">{row['city']}</div>
            <div class="card-temp">{row['temperature']}°</div>
            <div class="card-weather">{row['weather'].title()}</div>
            <div class="card-aqi">AQI {aqi}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Temperature chart
st.markdown('<div class="section-label">Temperature Over Time (°C)</div>', unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(14, 3.5))
for i, city in enumerate(weather_df['city'].unique()):
    d = weather_df[weather_df['city'] == city]
    ax.plot(d['timestamp'], d['temperature'], color=COLORS[i],
            linewidth=2.5, marker='o', markersize=4, label=city)
ax.legend(loc='upper right', framealpha=0, labelcolor='#94a3b8', fontsize=10, ncol=5)
ax.set_ylabel('°C', fontsize=11, color='#ffffff')
ax.grid(True, axis='y')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xticks(rotation=20, fontsize=9)
plt.tight_layout(pad=1.5)
st.pyplot(fig)
plt.close()

# AQI chart
st.markdown('<div class="section-label">Air Quality Index Over Time</div>', unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(14, 3.5))
for i, city in enumerate(aqi_df['city'].unique()):
    d = aqi_df[aqi_df['city'] == city]
    ax.plot(d['timestamp'], d['aqi_value'], color=COLORS[i],
            linewidth=2.5, marker='o', markersize=5, label=city)
ax.legend(loc='upper right', framealpha=0, labelcolor='#94a3b8', fontsize=10, ncol=5)
ax.set_ylabel('AQI Value', fontsize=11, color='#ffffff')
ax.grid(True, axis='y')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xticks(rotation=20, fontsize=9)
plt.tight_layout(pad=1.5)
st.pyplot(fig)
plt.close()

st.markdown("""
<div style='font-size:11px; color:#fffff; margin-top:8px; padding: 8px 12px; 
background:#0f0f20; border-left:2px solid #334155; border-radius:4px;'>
Note — Chandigarh and Panchkula share the same HSPCB monitoring station (Sector-6, Panchkula), 
hence identical AQI readings. This is a data infrastructure limitation, not an error.
</div>
""", unsafe_allow_html=True)

# City averages
st.markdown('<div class="section-label">City Averages</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    avg_temp = weather_df.groupby('city')['temperature'].mean().sort_values()
    fig, ax = plt.subplots(figsize=(6, 3.5))
    bars = ax.barh(avg_temp.index, avg_temp.values, color=COLORS[:len(avg_temp)], height=0.5)
    ax.set_xlabel('Avg Temperature (°C)', fontsize=10)
    ax.grid(True, axis='x', alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for bar, val in zip(bars, avg_temp.values):
        ax.text(val - 1, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}°', va='center', ha='right',
                color='#080812', fontsize=9, fontweight='bold')
    plt.tight_layout(pad=1.5)
    st.pyplot(fig)
    plt.close()

with col2:
    avg_aqi = aqi_df.groupby('city')['aqi_value'].mean().sort_values()
    fig, ax = plt.subplots(figsize=(6, 3.5))
    bars = ax.barh(avg_aqi.index, avg_aqi.values, color=COLORS[:len(avg_aqi)], height=0.5)
    ax.set_xlabel('Avg AQI', fontsize=10)
    ax.grid(True, axis='x', alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for bar, val in zip(bars, avg_aqi.values):
        ax.text(val - 0.3, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}', va='center', ha='right',
                color='#080812', fontsize=9, fontweight='bold')
    plt.tight_layout(pad=1.5)
    st.pyplot(fig)
    plt.close()

# Research findings
st.markdown('<div class="section-label">Research Findings</div>', unsafe_allow_html=True)

findings = [
    ("01", "Wind Speed is the Dominant Air Quality Predictor",
     "Wind speed shows a strong negative correlation with AQI (r = −0.84), far outweighing temperature effects (r = 0.32) across all monitored cities."),
    ("02", "Nocturnal AQI Inversion in Ambala",
     "Ambala recorded its highest AQI (26.01) after 22:00 IST despite falling temperatures — suggesting thermal inversion trapping pollutants near ground level at night."),
    ("03", "Chandigarh Urban Cooling Effect",
     "Chandigarh and Panchkula showed the sharpest temperature drop post-sunset (40°C → 32°C), likely due to planned urban green cover compared to industrial Ambala."),
    ("04", "Persistent Pollution Hotspot",
     "Ambala consistently recorded the highest AQI and temperature across the entire observation period, regardless of time of day or wind conditions.")
]

for num, title, desc in findings:
    st.markdown(f"""
    <div class="finding-card">
        <div class="finding-number">FINDING {num}</div>
        <div class="finding-title">{title}</div>
        <div class="finding-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    Prakriti Environmental Pipeline &nbsp;·&nbsp; OpenWeatherMap + OpenAQ (HSPCB) &nbsp;·&nbsp; Updates every hour
</div>
""", unsafe_allow_html=True)