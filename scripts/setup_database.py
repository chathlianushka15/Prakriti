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
engine = create_engine(f"postgresql://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

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