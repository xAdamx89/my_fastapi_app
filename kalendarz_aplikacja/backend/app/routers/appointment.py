from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
from ..db import cursor, conn
from ..email_utils import send_email


router = APIRouter()

class AppointmentCreate(BaseModel):
    name: str
    email: EmailStr
    start: datetime
    koniec: datetime
    note: str | None = None
    allDay: bool = False

@router.get("/appointments")
def get_appointments():
    cursor.execute("SELECT start, koniec FROM appointments")
    rows = cursor.fetchall()
    return [
        {
            "title": "Spotkanie - termin zajęty",
            "start": row[0].isoformat(),
            "end": row[1].isoformat()
        }
        for row in rows
    ]

@router.post("/appointments")
def add_appointment(appointment: AppointmentCreate):
    # Sprawdź kolizję terminów
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
            "INSERT INTO appointments (name, email, start, koniec, note, allday) VALUES (%s, %s, %s, %s, %s, %s)",
            (appointment.name, appointment.email, appointment.start, appointment.koniec, appointment.note, appointment.allDay)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Błąd serwera: {e}")

    # Wysyłanie maila z potwierdzeniem (nie blokuje odpowiedzi)
    try:
        send_email(
            to_email=appointment.email,
            subject="Potwierdzenie rezerwacji",
            body=f"Cześć {appointment.name},\n\nTwoja rezerwacja od {appointment.start} do {appointment.koniec} została przyjęta.\n\nDziękujemy!"
        )
    except Exception as e:
        print(f"Błąd wysyłki e-maila: {e}")

    return {"message": "Rezerwacja dodana"}