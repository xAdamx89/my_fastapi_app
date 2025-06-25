from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from psycopg2 import sql
from .db import cursor, pwd_context
import os
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr

load_dotenv()

auth_router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY", "tajny_klucz")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Modele Pydantic

class PasswordReset(BaseModel):
    username: str
    new_password: str

class User(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: str | None = None
    full_name: str | None = None

# Funkcje pomocnicze

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    try:
        cursor.execute("SELECT id, hashed_password FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        if not row:
            return False

        user_id, hashed_password = row
        if not verify_password(password, hashed_password):
            return False

        return User(username=username)
    except Exception as e:
        print("Błąd przy logowaniu:", e)
        return False

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpointy

@auth_router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Nieprawidłowe dane logowania")
    
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    try:
        # ... kod rejestracji ...
        cursor.connection.commit()
        return {"msg": "Użytkownik zarejestrowany"}
    except Exception as e:
        print("Błąd przy rejestracji:", e)
        raise HTTPException(status_code=500, detail="Błąd serwera")

# To musi być poza funkcją register:
@auth_router.post("/pass_reset")
async def reset_password(data: PasswordReset):
    try:
        cursor.execute("SELECT id FROM users WHERE username = %s", (data.username,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")

        hashed_password = pwd_context.hash(data.new_password)

        cursor.execute(
            "UPDATE users SET hashed_password = %s WHERE username = %s",
            (hashed_password, data.username)
        )
        cursor.connection.commit()

        return {"msg": "Hasło zostało zresetowane"}

    except Exception as e:
        print("Błąd przy resetowaniu hasła:", e)
        raise HTTPException(status_code=500, detail="Błąd serwera")