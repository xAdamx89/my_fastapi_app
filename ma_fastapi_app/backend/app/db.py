# backend/app/db.py

import psycopg2
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()  # Załaduj zmienne środowiskowe z .env

# Pobierz dane z .env lub podaj wartości domyślne
DB_NAME = os.getenv("DB_NAME", "rezerwacje")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "9089")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Ustaw połączenie
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
except Exception as e:
    print("❌ Błąd połączenia z bazą danych:", e)
    raise e

# Konfiguracja hashowania haseł
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")