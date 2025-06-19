from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from psycopg2 import sql
from app import cursor, pwd_context

auth_router = APIRouter()

# Tajne ustawienia JWT
SECRET_KEY = "tajny_klucz"  # zmień na zmienną środowiskową w produkcji
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Konfiguracja haseł
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

class User(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

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

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Nie można uwierzytelnić",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        # Możesz dodać sprawdzanie użytkownika w bazie
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        if not cursor.fetchone():
            raise credentials_exception

        return User(username=username)
    except JWTError:
        raise credentials_exception

@auth_router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Nieprawidłowe dane logowania")
    
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}
