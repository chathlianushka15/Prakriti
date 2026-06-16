import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("OPENAQ_API_KEY")

CITIES = [
    {"name": "Chandigarh", "lat": 30.7333, "lon": 76.7794},
    {"name": "Panchkula", "lat": 30.6942, "lon": 76.8606},
    {"name": "Ambala", "lat": 30.3752, "lon": 76.7821},
    {"name": "Kurukshetra", "lat": 29.9695, "lon": 76.8783},
    {"name": "Hisar", "lat": 29.1492, "lon": 75.7217}
]

def fetch_airquality(city):
    headers = {"X-API-Key": API_KEY}

    # Get nearest location
    url = f"https://api.openaq.org/v3/locations?coordinates={city['lat']},{city['lon']}&radius=25000&limit=1"
    response = requests.get(url, headers=headers)
    data = response.json()

    if not data.get("results"):
        return {"city": city["name"], "aqi_value": None, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    location = data["results"][0]
    location_id = location["id"]

    # Get latest readings
    meas_url = f"https://api.openaq.org/v3/locations/{location_id}/latest"
    meas_response = requests.get(meas_url, headers=headers)
    meas_data = meas_response.json()

    # Just grab first available value
    aqi_value = None
    if meas_data.get("results"):
        aqi_value = meas_data["results"][0]["value"]

    return {
        "city": city["name"],
        "aqi_value": aqi_value,
        "location_name": location.get("name", "Unknown"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    results = []

    for city in CITIES:
        result = fetch_airquality(city)
        print(result)
        results.append(result)

    df = pd.DataFrame(results)
    df.to_csv("data/airquality_data.csv", index=False)
    print("\n✅ Air quality data saved to data/airquality_data.csv")