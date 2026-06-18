import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_USER = os.getenv("DB_USER", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

from urllib.parse import quote_plus
password = quote_plus(DB_PASSWORD)
SUPA_HOST = os.getenv("SUPABASE_HOST")
SUPA_DB = os.getenv("SUPABASE_DB")
SUPA_USER = os.getenv("SUPABASE_USER")
SUPA_PASSWORD = quote_plus(os.getenv("SUPABASE_PASSWORD"))
SUPA_PORT = os.getenv("SUPABASE_PORT")

engine = create_engine(f"postgresql://{SUPA_USER}:{SUPA_PASSWORD}@{SUPA_HOST}:{SUPA_PORT}/{SUPA_DB}")

def setup():
    with engine.connect() as conn:
        # Weather table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS weather (
                id SERIAL PRIMARY KEY,
                city VARCHAR(100),
                temperature FLOAT,
                humidity INTEGER,
                weather VARCHAR(200),
                wind_speed FLOAT,
                timestamp TIMESTAMP
            )
        """))

        # Air quality table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS airquality (
                id SERIAL PRIMARY KEY,
                city VARCHAR(100),
                aqi_value FLOAT,
                location_name VARCHAR(200),
                timestamp TIMESTAMP
            )
        """))

        conn.commit()
        print("✅ Tables created successfully in Prakriti database")

if __name__ == "__main__":
    setup()