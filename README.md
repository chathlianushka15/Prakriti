<div align="center">

<img src="https://img.shields.io/badge/🌿_PRAKRITI-Environmental_Intelligence-1D9E75?style=for-the-badge&labelColor=085041" />

```
प्रकृति  ·  prakriti  ·  /prʌkrɪti/  ·  Sanskrit: "nature" or "the natural world"
```

[![Live Dashboard](https://img.shields.io/badge/⚡_Live_Dashboard-prakriti--env.streamlit.app-ff6b9d?style=for-the-badge)](https://prakriti-env.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-7ecba1?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-a78bfa?style=for-the-badge&logo=postgresql&logoColor=white)](https://supabase.com)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-60a5fa?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)

---

### *A research-grade environmental intelligence pipeline monitoring air quality and weather across the Chandigarh – Haryana corridor  in real time.*

</div>

---

## 🛰️ What is Prakriti?

Prakriti is a **continuous environmental data pipeline** that ingests live weather and air quality readings from government-grade sensors (HSPCB) and OpenWeatherMap, stores them in a cloud PostgreSQL database, and surfaces insights through an interactive Streamlit dashboard.

It was built as an independent research project to investigate the relationship between meteorological variables and air quality patterns across 5 cities in North India - and it runs **24/7**, silently logging the atmosphere.

---

## 🔬 Key Research Findings

> From 24 hours of continuous monitoring across 5 cities - these are the findings that stood out.

| # | Finding | Signal |
|---|---------|--------|
| 🌬️ | **Wind is the dominant AQI driver** | Pearson r = **−0.84** between wind speed and AQI |
| 🔥 | **Ambala is a persistent pollution hotspot** | Highest avg temp (38.53°C) *and* avg AQI (18.40) |
| 🌙 | **Nocturnal AQI inversion detected** | Ambala AQI spiked to **26.01 at 22:00 IST** despite falling temperatures |
| 🏙️ | **Chandigarh shows urban cooling effect** | Sharpest post-sunset drop observed: 40°C → 32°C |
| 📉 | **Temperature is a weak AQI predictor** | r = 0.32 — far below wind speed's effect |

> **TL;DR:** Open your windows when it's windy. Wind disperses pollution far more effectively than temperature alone.

---

## 🗺️ Cities Monitored

| City | Avg Temp | Avg AQI (PM2.5) | HSPCB Monitoring Station |
|------|----------|-----------------|--------------------------|
| 🔵 Chandigarh | 36.9°C | 10.8 | Sector-6, Panchkula |
| 🟢 Panchkula | 36.8°C | 10.8 | Sector-6, Panchkula |
| 🔴 Ambala | 38.4°C | **17.9** ← highest | Patti Mehar, Ambala |
| 🟡 Kurukshetra | 38.7°C | 9.7 | Sector-7, Kurukshetra |
| 🟠 Hisar | 37.3°C | 15.7 | Urban Estate-II, Hisar |

---

## ⚙️ How It Works

```
┌─────────────────────┐          ┌──────────────────────────────┐
│  OpenWeatherMap API │          │  OpenAQ API (HSPCB Sensors)  │
│  temp · humidity    │          │  PM2.5 · AQI readings        │
│  wind · conditions  │          │  from govt. ground stations  │
└────────┬────────────┘          └────────────┬─────────────────┘
         │                                    │
         ▼                                    ▼
  fetch_weather.py                   fetch_airquality.py
         │                                    │
         └──────────────┬─────────────────────┘
                        │
                        ▼
              scheduler.py  ──── runs every hour ────►  logs to console
                        │
                        ▼
           Supabase PostgreSQL
           (cloud-hosted, persistent)
                        │
                        ▼
           combine.py + analyze.py
           (merge, correlate, detect anomalies)
                        │
                        ▼
            Streamlit Dashboard
            (live at prakriti-env.streamlit.app)
```

---

## 🧰 Tech Stack

| Layer | Tool | Why |
|-------|------|-----|
| 🔌 Data Ingestion | Python + Requests | Lightweight HTTP client for REST APIs |
| 🧹 Processing | Pandas | Fast DataFrame operations for merging & stats |
| 🗄️ Storage | PostgreSQL via Supabase | Free-tier cloud DB with SQL querying |
| ⏰ Scheduling | `schedule` library | Pure-Python cron without system dependencies |
| 📊 Dashboard | Streamlit | Rapid data app deployment in Python |
| ☁️ Deployment | Streamlit Cloud | Free hosting with GitHub auto-deploy |

---

## 📁 Project Structure

```
prakriti/
│
├── scripts/
│   ├── fetch_weather.py        # 🌤  Pulls temp, humidity, wind from OpenWeatherMap
│   ├── fetch_airquality.py     # 💨  Pulls PM2.5/AQI from OpenAQ (HSPCB sensors)
│   ├── scheduler.py            # ⏰  Runs the full pipeline every hour
│   ├── combine.py              # 🔗  Merges weather + AQI into unified dataset
│   ├── analyze.py              # 📈  Correlation analysis + anomaly detection
│   └── setup_database.py       # 🗄  Creates Supabase schema on first run
│
├── dashboards/
│   └── app.py                  # 📊  Streamlit dashboard (the public-facing UI)
│
├── notebooks/
│   └── prakriti_research.ipynb # 🔬  Deep-dive analysis + visualizations
│
├── data/                       # 💾  CSV backups of ingested data
└── .env.example                # 🔑  API key template
```

---

## 🚀 Getting Started

### 1. Clone & set up environment

```bash
git clone https://github.com/chathlianushka15/Prakriti
cd prakriti

conda create -n prakriti python=3.11
conda activate prakriti

pip install requests pandas psycopg2-binary sqlalchemy \
            python-dotenv schedule streamlit matplotlib
```

### 2. Configure API keys

```bash
cp .env.example .env
# Open .env and add:
#   OPENWEATHERMAP_API_KEY=your_key_here
#   SUPABASE_URL=your_supabase_url
#   SUPABASE_KEY=your_supabase_key
```

> Get a free OpenWeatherMap key at [openweathermap.org/api](https://openweathermap.org/api) · Supabase project at [supabase.com](https://supabase.com)

### 3. Initialize the database

```bash
python scripts/setup_database.py
```

### 4. Start the pipeline

```bash
python scripts/scheduler.py
# The pipeline now runs every hour, logging weather + AQI to your database.
```

### 5. Launch the dashboard locally (optional)

```bash
streamlit run dashboards/app.py
# Or just visit: https://prakriti-env.streamlit.app
```

---

## 📡 Data Sources

| Source | Data | Coverage |
|--------|------|----------|
| [OpenWeatherMap API](https://openweathermap.org/api) | Temperature, humidity, wind speed, weather description | Global |
| [OpenAQ API](https://openaq.org) | PM2.5 / AQI readings from HSPCB ground sensors | Haryana & Chandigarh |

> **HSPCB** = Haryana State Pollution Control Board — government-operated monitoring network.

---

## 🔭 What's Next

- [ ] Extend monitoring to Delhi NCR and Punjab
- [ ] Add PM10, NO₂, SO₂ pollutant tracking
- [ ] Build a 24-hour AQI forecast model using the collected data
- [ ] Alert system for when AQI crosses hazardous thresholds
- [ ] Publish findings as a research brief

---

## 👩‍💻 Author

**Anushka** - 3rd year CSE student with a research focus on Environmental Informatics and Data Engineering.

Built independently as a research project to understand the interplay between meteorology and air quality in the Chandigarh–Haryana region, using real government sensor data and a fully automated cloud pipeline.

> *"The wind doesn't just bring weather - it determines how clean the air you breathe is."*

---

<div align="center">

Made with 🌿 + Python · Running 24/7 · Watching the sky

[![Visit Dashboard](https://img.shields.io/badge/Visit_Live_Dashboard-→-1D9E75?style=for-the-badge)](https://prakriti-env.streamlit.app)

</div>