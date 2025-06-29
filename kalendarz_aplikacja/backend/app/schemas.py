from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserCreate(BaseModel):
    username: constr(min_length=3)
    email: EmailStr
    password: constr(min_length=6)

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

class Config:
    orm_mode = True

class RegisterUser(BaseModel):
    username: constr(min_length=1, max_length=50)
    email: EmailStr
    password: constr(min_length=1, max_length=100)
    full_name: Optional[constr(max_length=100)] = None