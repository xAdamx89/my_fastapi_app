from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = psycopg2.connect(
    dbname="rezerwacje",
    user="postgres",
    password="9089",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

class Apointment(BaseModel):
    name: str
    email: str
    date: str  # YYYY-MM-DD

# GET - pobieranie terminów
@app.get("/appointments")
def get_appointments():
    cursor.execute("SELECT date FROM appointments")
    rows = cursor.fetchall()
    return [{"title": "Spotkanie - termin zajęty", "date": str(row[0])} for row in rows]

# POST - dodawanie nowego terminu
@app.post("/appointments")
def add_appointment(appointment: Apointment):
    try:
        cursor.execute(
            "INSERT INTO appointments (name, email, date) VALUES (%s, %s, %s)",
            (appointment.name, appointment.email, appointment.date)
        )
        conn.commit()
        return {"message": "Rezerwacja dodana"}
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Termin już zajęty")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
def root():
    return {"message": "API działa"}
