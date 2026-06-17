import sqlalchemy
import pandas as pd
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

engine = sqlalchemy.create_engine(
    f'postgresql://postgres:{quote_plus(os.getenv("DB_PASSWORD"))}@localhost/prakriti'
)

df = pd.read_sql('SELECT city, temperature, timestamp FROM weather ORDER BY timestamp ASC', engine)
print(df.to_string())