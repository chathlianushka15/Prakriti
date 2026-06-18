import pandas as pd
import sqlalchemy
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

# Local database
local_password = quote_plus(os.getenv("DB_PASSWORD"))
local_engine = sqlalchemy.create_engine(
    f'postgresql://postgres:{local_password}@localhost/prakriti'
)

# Supabase database
supa_password = quote_plus(os.getenv("SUPABASE_PASSWORD"))
supa_engine = sqlalchemy.create_engine(
    f'postgresql://{os.getenv("SUPABASE_USER")}:{supa_password}@{os.getenv("SUPABASE_HOST")}:{os.getenv("SUPABASE_PORT")}/{os.getenv("SUPABASE_DB")}'
)

# Migrate weather data
print("Migrating weather data...")
weather_df = pd.read_sql('SELECT * FROM weather', local_engine)
weather_df = weather_df.drop(columns=['id'])
weather_df.to_sql('weather', supa_engine, if_exists='append', index=False)
print(f"✅ Migrated {len(weather_df)} weather rows")

# Migrate air quality data
print("Migrating air quality data...")
aqi_df = pd.read_sql('SELECT * FROM airquality', local_engine)
aqi_df = aqi_df.drop(columns=['id'])
aqi_df.to_sql('airquality', supa_engine, if_exists='append', index=False)
print(f"✅ Migrated {len(aqi_df)} air quality rows")

print("\n✅ Migration complete!")