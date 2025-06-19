from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel

auth_router = APIRouter()

# Tajne ustawienia JWT
SECRET_KEY = "tajny_klucz"  # zmień na zmienną środowiskową w produkcji
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Konfiguracja haseł
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Tymczasowy użytkownik (zastąp bazą danych)
FAKE_ADMIN = {
    "username": "admin",
    "hashed_password": pwd_context.hash("admin123")
}

class User(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def authenticate_user(username: str, password: str):
    if username != FAKE_ADMIN["username"]:
        return False
    if not verify_password(password, FAKE_ADMIN["hashed_password"]):
        return False
    return User(username=username)

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
        if username != FAKE_ADMIN["username"]:
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
