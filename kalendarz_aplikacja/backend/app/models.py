# backend/app/models.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class AppointmentCreate(BaseModel):
    name: str
    email: str
    start: datetime
    koniec: datetime
    allDay: bool
    note: Optional[str] = None