from fastapi import FastAPI
from app import models, database
from app.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI
import logging

from fastapi import FastAPI
from app.auth import router as auth_router

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

from app import models, database

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import psycopg2
import uuid

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(auth_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

app.include_router(auth_router)

origins = [
            "http://amfm.pl",
        "http://www.amfm.pl",
        "http://api.amfm.pl",
        "http://46.205.243.253",
        "http://192.168.1.3"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AppointmentBase(BaseModel):
    name: str
    email: EmailStr
    start: datetime
    koniec: datetime
    note: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentOut(AppointmentBase):
    id: int

    class Config:
        orm_mode = True
        
# Pobranie sesji bazy danych
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model
class Reservation(BaseModel):
    name: str
    email: str
    start: str
    koniec: str
    note: str = ""
    allDay: bool = False

@app.get("/appointments", response_model=List[AppointmentOut])
def get_appointments(db: Session = Depends(get_db)):
    appointments = db.query(models.Appointment).all()
    return appointments

@app.post("/appointments", status_code=status.HTTP_201_CREATED)
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db)):
    # Sprawdź czy termin się nie pokrywa z istniejącymi
    overlapping = db.query(models.Appointment).filter(
        models.Appointment.start < data.koniec,
        models.Appointment.koniec > data.start
    ).first()
    if overlapping:
        raise HTTPException(status_code=400, detail="Termin jest już zajęty")

    appointment = models.Appointment(
        name=data.name,
        email=data.email,
        start=data.start,
        koniec=data.koniec,
        note=data.note
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return {"message": "Rezerwacja utworzona pomyślnie."}

conn = psycopg2.connect(
    dbname="rezerwacje", user="postgres", password="9089", host="localhost", port="5432"
)
cursor = conn.cursor()

@app.get("/reservations")
def get_reservations():
    cursor.execute("SELECT id, name, email, start, koniec, note FROM appointments")
    rows = cursor.fetchall()
    return [
        {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "start": row[3],
            "koniec": row[4],
            "note": row[5],
        }
        for row in rows
    ]

# Dodaj rezerwację
@app.post("/appointments")
def create_reservation(reservation: Reservation):
    new_id = str(uuid.uuid4())
    cursor.execute(
        "INSERT INTO appointments (id, name, email, start, koniec, note, allday) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (
            new_id,
            reservation.name,
            reservation.email,
            reservation.start,
            reservation.koniec,
            reservation.note,
            reservation.allDay,
        ),
    )
    conn.commit()
    return {"id": new_id}

# Usuń rezerwację
@app.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: str):
    cursor.execute("DELETE FROM appointments WHERE id = %s", (reservation_id,))
    conn.commit()
    return {"message": "Deleted"}

# Edytuj rezerwację
@app.put("/reservations/{reservation_id}")
def update_reservation(reservation_id: str, reservation: Reservation):
    cursor.execute(
        "UPDATE appointments SET name = %s, email = %s, start = %s, koniec = %s, note = %s, allday = %s WHERE id = %s",
        (
            reservation.name,
            reservation.email,
            reservation.start,
            reservation.koniec,
            reservation.note,
            reservation.allDay,
            reservation_id,
        ),
    )
    conn.commit()
    return {"message": "Updated"}

