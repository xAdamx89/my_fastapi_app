from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
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

class Apointment(BaseModel):
    name: str
    email: str
    date: str  # YYYY-MM-DD

# GET - pobieranie tylko zajętych dat
@app.get("/appointments")
def get_appointments():
    cursor.execute("SELECT date FROM appointments")
    rows = cursor.fetchall()
    return [{"title": "Spotkanie - termin zajęty", "date": str(row[0])} for row in rows]

# POST - dodawanie nowej rezerwacji
@app.post("/appointments")
def add_appointment(appointment: Apointment):
    try:
        cursor.execute(
            "INSERT INTO appointments (name, email, date) VALUES (%s, %s, %s)",
            (appointment.name, appointment.email, appointment.date)
        )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Termin już zajęty")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    # Próba wysłania maila — nie blokuj dodania rezerwacji, jeśli mail się nie wyśle
    try:
        send_email(
            to_email=appointment.email,
            subject="Potwierdzenie rezerwacji",
            body=f"Cześć {appointment.name},\n\nTwoja rezerwacja na {appointment.date} została przyjęta.\n\nDziękujemy!"
        )
    except Exception as e:
        # Możesz zalogować błąd wysyłki maila, ale nie przerywaj działania endpointu
        print(f"Błąd wysyłki e-maila: {e}")

    return {"message": "Rezerwacja dodana"}

# GET - wszystkie rezerwacje
@app.get("/reservations")
def get_all_reservations():
    cursor.execute("SELECT id, name, email, date FROM appointments")
    rows = cursor.fetchall()
    return [
        {"id": row[0], "name": row[1], "email": row[2], "date": str(row[3])}
        for row in rows
    ]

# DELETE - usuwanie rezerwacji
@app.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int):
    cursor.execute("SELECT name, email, date FROM appointments WHERE id = %s", (reservation_id,))
    reservation = cursor.fetchone()

    if not reservation:
        raise HTTPException(status_code=404, detail="Rezerwacja nie istnieje")

    cursor.execute("DELETE FROM appointments WHERE id = %s", (reservation_id,))
    conn.commit()

    send_email(
        to_email=reservation[1],
        subject="Rezerwacja odwołana",
        body=f"Cześć {reservation[0]},\n\nTwoja rezerwacja na {reservation[2]} została odwołana przez administratora."
    )

    return {"message": "Rezerwacja usunięta"}

# PUT - edycja rezerwacji
@app.put("/reservations/{reservation_id}")
def update_reservation(reservation_id: int, appointment: Apointment):
    cursor.execute("SELECT name, email, date FROM appointments WHERE id = %s", (reservation_id,))
    old = cursor.fetchone()

    if not old:
        raise HTTPException(status_code=404, detail="Rezerwacja nie istnieje")

    cursor.execute(
        "UPDATE appointments SET name = %s, email = %s, date = %s WHERE id = %s",
        (appointment.name, appointment.email, appointment.date, reservation_id)
    )
    conn.commit()

    send_email(
        to_email=appointment.email,
        subject="Rezerwacja zmodyfikowana",
        body=f"Cześć {appointment.name},\n\nTwoja rezerwacja została zmodyfikowana.\nNowa data: {appointment.date}."
    )

    return {"message": "Rezerwacja zaktualizowana"}

@app.get("/")
def root():
    return {"message": "API działa"}
