import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAQ_API_KEY")
headers = {"X-API-Key": API_KEY}

r = requests.get("https://api.openaq.org/v3/locations?coordinates=30.7333,76.7794&radius=25000&limit=1", headers=headers)
data = r.json()
location_id = data["results"][0]["id"]

r2 = requests.get(f"https://api.openaq.org/v3/locations/{location_id}/latest", headers=headers)
print(json.dumps(r2.json()["results"][0], indent=2))