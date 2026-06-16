import schedule
import time
import subprocess
from datetime import datetime

def run_weather():
    print(f"\n🌤️ Fetching weather at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    subprocess.run(["python", "scripts/fetch_weather.py"])
    print("✅ Weather done")

def run_airquality():
    print(f"\n🌿 Fetching air quality at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    subprocess.run(["python", "scripts/fetch_airquality.py"])
    print("✅ Air quality done")

def run_pipeline():
    run_weather()
    run_airquality()
    print(f"\n✅ Full pipeline complete at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

# Schedule every hour
schedule.every(1).hours.do(run_pipeline)

# Run immediately on start
print("🌿 Prakriti pipeline started. Running every hour...")
print("-" * 50)
run_pipeline()

while True:
    schedule.run_pending()
    time.sleep(60)