# backend/app/db.py
import psycopg2
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname="rezerwacje",
    user="postgres",
    password="9089",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
