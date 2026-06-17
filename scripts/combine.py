import pandas as pd
from datetime import datetime

def combine_data():
    # Load both datasets
    weather = pd.read_csv("data/weather_data.csv")
    airquality = pd.read_csv("data/airquality_data.csv")

    # Merge on city name
    combined = pd.merge(weather, airquality, on="city", suffixes=("_weather", "_aqi"))

    # Clean up timestamp columns
    combined = combined.rename(columns={
        "timestamp_weather": "timestamp",
        "timestamp_aqi": "aqi_timestamp"
    })

    # Save combined dataset
    combined.to_csv("data/combined_data.csv", index=False)
    print(combined.to_string())
    print(f"\n✅ Combined data saved at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    combine_data()