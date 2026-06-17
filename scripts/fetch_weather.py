import requests
import os
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

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

    # Save to CSV
    df = pd.DataFrame(results)
    df.to_csv("data/weather_data.csv", index=False)

    # Save to database
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.to_sql("weather", engine, if_exists="append", index=False)

    print("\n✅ Weather data saved to CSV and database")