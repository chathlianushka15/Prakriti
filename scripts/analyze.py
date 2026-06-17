import pandas as pd
import json
from datetime import datetime

def analyze():
    df = pd.read_csv("data/combined_data.csv")

    print("=" * 50)
    print("🌿 PRAKRITI — ENVIRONMENTAL ANALYSIS")
    print("=" * 50)

    # 1. Basic stats
    print("\n📊 TEMPERATURE SUMMARY (°C)")
    print(df[["city", "temperature"]].to_string(index=False))

    print("\n💧 HUMIDITY SUMMARY (%)")
    print(df[["city", "humidity"]].to_string(index=False))

    print("\n🌫️ AIR QUALITY SUMMARY (AQI)")
    print(df[["city", "aqi_value"]].to_string(index=False))

    # 2. Hottest and coolest city
    hottest = df.loc[df["temperature"].idxmax()]
    coolest = df.loc[df["temperature"].idxmin()]
    print(f"\n🔥 Hottest city: {hottest['city']} at {hottest['temperature']}°C")
    print(f"❄️  Coolest city: {coolest['city']} at {coolest['temperature']}°C")

    # 3. Most and least polluted
    most_polluted = df.loc[df["aqi_value"].idxmax()]
    cleanest = df.loc[df["aqi_value"].idxmin()]
    print(f"\n😷 Most polluted: {most_polluted['city']} with AQI {most_polluted['aqi_value']}")
    print(f"✅ Cleanest air: {cleanest['city']} with AQI {cleanest['aqi_value']}")

    # 4. Correlation between temperature and AQI
    correlation = df["temperature"].corr(df["aqi_value"])
    print(f"\n🔬 Correlation between temperature and AQI: {correlation:.2f}")
    if correlation > 0.5:
        print("   → Higher temperature linked to worse air quality")
    elif correlation < -0.5:
        print("   → Higher temperature linked to better air quality")
    else:
        print("   → No strong correlation found yet (need more data)")

    # 5. Anomaly detection — cities with unusually high AQI
    mean_aqi = df["aqi_value"].mean()
    std_aqi = df["aqi_value"].std()
    print(f"\n⚠️  ANOMALY DETECTION")
    print(f"   Mean AQI: {mean_aqi:.2f} | Std Dev: {std_aqi:.2f}")
    anomalies = df[df["aqi_value"] > mean_aqi + std_aqi]
    if not anomalies.empty:
        print(f"   🚨 Anomalies detected in: {', '.join(anomalies['city'].tolist())}")
    else:
        print("   ✅ No anomalies detected")

    # Save summary
    summary = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hottest_city": hottest["city"],
        "coolest_city": coolest["city"],
        "most_polluted": most_polluted["city"],
        "cleanest": cleanest["city"],
        "temp_aqi_correlation": round(correlation, 2),
        "anomalies": anomalies["city"].tolist()
    }

    with open("data/analysis_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n✅ Analysis saved to data/analysis_summary.json")
    print("=" * 50)

if __name__ == "__main__":
    analyze()