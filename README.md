\# 🌿 Prakriti — Environmental Data Pipeline



A real-time environmental monitoring pipeline that collects weather and air quality data across Chandigarh and Haryana cities.



\## 📡 Data Sources

\- \*\*OpenWeatherMap API\*\* — Live weather data (temperature, humidity, wind speed)

\- \*\*OpenAQ API\*\* — Real air quality readings from HSPCB government sensors



\## 🏙️ Cities Monitored

\- Chandigarh

\- Panchkula

\- Ambala

\- Kurukshetra

\- Hisar



\## 🛠️ Tech Stack

\- Python 3.11

\- Pandas — data processing

\- Schedule — pipeline automation

\- PostgreSQL — database (coming soon)

\- Streamlit — dashboard (coming soon)



\## 📁 Project Structure

prakriti/



├── scripts/



│   ├── fetch\_weather.py       # Weather data pipeline



│   ├── fetch\_airquality.py    # Air quality pipeline



│   └── scheduler.py           # Runs both every hour



├── data/                      # Collected CSV data



├── dashboards/                # Frontend (coming soon)



├── notebooks/                 # Analysis notebooks



├── logs/                      # Pipeline logs



├── .env.example               # API key template



└── README.md



\## 🚀 Setup



1\. Clone the repo

2\. Create a virtual environment



conda create -n prakriti python=3.11



conda activate prakriti

3\. Install dependencies

pip install requests pandas psycopg2-binary sqlalchemy python-dotenv schedule

4\. Copy `.env.example` to `.env` and add your API keys

5\. Run the pipeline

python scripts/scheduler.py



\## 🔬 Research Angles

\- Correlation between temperature and air quality

\- Anomaly detection in pollution levels

\- Urban vs semi-urban environmental comparison across Haryana



\## 👩‍💻 Author

Built as part of an Environmental Informatics + Data Engineering research project.

