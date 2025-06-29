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

@router.get("/reservations")
def get_all_reservations():
    cursor.execute("SELECT id, name, email, start, koniec, note FROM appointments")
    rows = cursor.fetchall()
    return [
        {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "start": row[3].isoformat(),
            "koniec": row[4].isoformat(),
            "note": row[5],
        }
        for row in rows
    ]

@router.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int):
    cursor.execute("SELECT name, email, start, koniec FROM appointments WHERE id = %s", (reservation_id,))
    reservation = cursor.fetchone()

    if not reservation:
        raise HTTPException(status_code=404, detail="Rezerwacja nie istnieje")

    cursor.execute("DELETE FROM appointments WHERE id = %s", (reservation_id,))
    conn.commit()

    # Wysyłanie maila o anulowaniu rezerwacji (nie blokujemy endpointu)
    try:
        send_email(
            to_email=reservation[1],
            subject="Rezerwacja odwołana",
            body=f"Cześć {reservation[0]},\n\nTwoja rezerwacja od {reservation[2]} do {reservation[3]} została odwołana przez administratora."
        )
    except Exception as e:
        print(f"Błąd wysyłki e-maila: {e}")

    return {"message": "Rezerwacja usunięta"}

@router.put("/reservations/{reservation_id}")
def update_reservation(reservation_id: int, appointment: AppointmentCreate):
    cursor.execute("SELECT name, email, start, koniec FROM appointments WHERE id = %s", (reservation_id,))
    old = cursor.fetchone()

    if not old:
        raise HTTPException(status_code=404, detail="Rezerwacja nie istnieje")

    # Sprawdzenie kolizji z innymi rezerwacjami (poza tą edytowaną)
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
        "UPDATE appointments SET name = %s, email = %s, start = %s, koniec = %s, note = %s, allday = %s WHERE id = %s",
        (appointment.name, appointment.email, appointment.start, appointment.koniec, appointment.note, appointment.allDay, reservation_id)
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