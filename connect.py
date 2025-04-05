import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Загружаем переменные окружения или используем значения по умолчанию
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "8888")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def set_connection():
    engine = create_engine(DATABASE_URL)
    return engine.connect()
