import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

CITIES = ["Chandigarh", "Panchkula", "Ambala", "Kurukshetra", "Hisar"]


def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


if __name__ == "__main__":
    results = []

    for city in CITIES:
        result = fetch_weather(city)
        print(result)
        results.append(result)

    df = pd.DataFrame(results)
    df.to_csv("data/weather_data.csv", index=False)
    print("\n✅ Data saved to data/weather_data.csv")