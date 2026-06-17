import pandas as pd
import json
import os
import sqlalchemy
from urllib.parse import quote_plus
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def analyze():
    DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
    engine = sqlalchemy.create_engine(
        f'postgresql://postgres:{DB_PASSWORD}@localhost/prakriti'
    )
    weather_df = pd.read_sql('SELECT * FROM weather ORDER BY timestamp ASC', engine)
    aqi_df = pd.read_sql('SELECT * FROM airquality ORDER BY timestamp ASC', engine)
    df = pd.merge(weather_df, aqi_df, on='city', suffixes=('_weather', '_aqi'))

    print("=" * 50)
    print("PRAKRITI — ENVIRONMENTAL ANALYSIS")
    print("=" * 50)

    print("\nTEMPERATURE SUMMARY (C)")
    print(df.groupby("city")["temperature"].mean().round(2).to_string())

    print("\nHUMIDITY SUMMARY (%)")
    print(df.groupby("city")["humidity"].mean().round(2).to_string())

    print("\nAIR QUALITY SUMMARY (AQI)")
    print(df.groupby("city")["aqi_value"].mean().round(2).to_string())

    hottest = df.loc[df["temperature"].idxmax()]
    coolest = df.loc[df["temperature"].idxmin()]
    print(f"\nHottest city: {hottest['city']} at {hottest['temperature']}C")
    print(f"Coolest city: {coolest['city']} at {coolest['temperature']}C")

    most_polluted = df.loc[df["aqi_value"].idxmax()]
    cleanest = df.loc[df["aqi_value"].idxmin()]
    print(f"\nMost polluted: {most_polluted['city']} with AQI {most_polluted['aqi_value']}")
    print(f"Cleanest air: {cleanest['city']} with AQI {cleanest['aqi_value']}")

    correlation = df["temperature"].corr(df["aqi_value"])
    print(f"\nCorrelation between temperature and AQI: {correlation:.2f}")
    if correlation > 0.5:
        print("   Higher temperature linked to worse air quality")
    elif correlation < -0.5:
        print("   Higher temperature linked to better air quality")
    else:
        print("   No strong correlation found yet")

    mean_aqi = df["aqi_value"].mean()
    std_aqi = df["aqi_value"].std()
    print(f"\nANOMALY DETECTION")
    print(f"   Mean AQI: {mean_aqi:.2f} | Std Dev: {std_aqi:.2f}")
    anomalies = df[df["aqi_value"] > mean_aqi + std_aqi]
    if not anomalies.empty:
        print(f"   Anomalies detected in: {', '.join(anomalies['city'].unique().tolist())}")
    else:
        print("   No anomalies detected")

    summary = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hottest_city": hottest["city"],
        "coolest_city": coolest["city"],
        "most_polluted": most_polluted["city"],
        "cleanest": cleanest["city"],
        "temp_aqi_correlation": round(correlation, 2),
        "anomalies": anomalies["city"].unique().tolist()
    }

    with open("data/analysis_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nAnalysis saved to data/analysis_summary.json")
    print("=" * 50)

if __name__ == "__main__":
    analyze()