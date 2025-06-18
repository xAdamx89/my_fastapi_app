from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import psycopg2
from psycopg2 import sql
from fastapi.middleware.cors import CORSMiddleware
from email_utils import send_email
from dotenv import load_dotenv
import os

load_dotenv()
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

class AppointmentCreate(BaseModel):
    name: str
    email: str
    start: datetime
    koniec: datetime

@app.get("/appointments")
def get_appointments():
    cursor.execute("SELECT start, koniec FROM appointments")
    rows = cursor.fetchall()
    # Zamień daty na ISO string, żeby FullCalendar mógł je dobrze interpretować
    return [
        {
            "title": "Spotkanie - termin zajęty",
            "start": row[0].isoformat(),
            "end": row[1].isoformat()
        } for row in rows
    ]

@app.post("/appointments")
def add_appointment(appointment: AppointmentCreate):
    # Sprawdź kolizję terminów (overlapping)
    cursor.execute(
        """
        SELECT 1 FROM appointments
        WHERE (start, koniec) OVERLAPS (%s, %s)
        """,
        (appointment.start, appointment.koniec)
    )
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Termin już zajęty")

    try:
        cursor.execute(
            "INSERT INTO appointments (name, email, start, koniec) VALUES (%s, %s, %s, %s)",
            (appointment.name, appointment.email, appointment.start, appointment.koniec)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    # Wysyłanie maila (nie blokuj endpointu, jeśli mail się nie wyśle)
    try:
        send_email(
            to_email=appointment.email,
            subject="Potwierdzenie rezerwacji",
            body=f"Cześć {appointment.name},\n\nTwoja rezerwacja od {appointment.start} do {appointment.koniec} została przyjęta.\n\nDziękujemy!"
        )
    except Exception as e:
        print(f"Błąd wysyłki e-maila: {e}")

    return {"message": "Rezerwacja dodana"}

@app.get("/reservations")
def get_all_reservations():
    cursor.execute("SELECT id, name, email, start, koniec FROM appointments")
    rows = cursor.fetchall()
    return [
        {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "start": row[3].isoformat(),
            "koniec": row[4].isoformat()
        }
        for row in rows
    ]

@app.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int):
    cursor.execute("SELECT name, email, start, koniec FROM appointments WHERE id = %s", (reservation_id,))
    reservation = cursor.fetchone()

    if not reservation:
        raise HTTPException(status_code=404, detail="Rezerwacja nie istnieje")

    cursor.execute("DELETE FROM appointments WHERE id = %s", (reservation_id,))
    conn.commit()

    try:
        send_email(
            to_email=reservation[1],
            subject="Rezerwacja odwołana",
            body=f"Cześć {reservation[0]},\n\nTwoja rezerwacja od {reservation[2]} do {reservation[3]} została odwołana przez administratora."
        )
    except Exception as e:
        print(f"Błąd wysyłki e-maila: {e}")

    return {"message": "Rezerwacja usunięta"}

@app.put("/reservations/{reservation_id}")
def update_reservation(reservation_id: int, appointment: AppointmentCreate):
    cursor.execute("SELECT name, email, start, koniec FROM appointments WHERE id = %s", (reservation_id,))
    old = cursor.fetchone()

    if not old:
        raise HTTPException(status_code=404, detail="Rezerwacja nie istnieje")

    # Sprawdź czy nowy termin się nie nakłada na inne rezerwacje (oprócz tej edytowanej)
    cursor.execute(
        """
        SELECT 1 FROM appointments
        WHERE id != %s AND (start, koniec) OVERLAPS (%s, %s)
        """,
        (reservation_id, appointment.start, appointment.koniec)
    )
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Termin już zajęty")

    cursor.execute(
        "UPDATE appointments SET name = %s, email = %s, start = %s, koniec = %s WHERE id = %s",
        (appointment.name, appointment.email, appointment.start, appointment.koniec, reservation_id)
    )
    conn.commit()

    try:
        send_email(
            to_email=appointment.email,
            subject="Rezerwacja zmodyfikowana",
            body=f"Cześć {appointment.name},\n\nTwoja rezerwacja została zmodyfikowana.\nNowy termin od {appointment.start} do {appointment.koniec}."
        )
    except Exception as e:
        print(f"Błąd wysyłki e-maila: {e}")

    return {"message": "Rezerwacja zaktualizowana"}

@app.get("/")
def root():
    return {"message": "API działa"}
