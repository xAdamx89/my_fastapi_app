@echo off
REM Przejd� do katalogu, gdzie jest venv
cd /d C:\kalendarz_aplikacja || (
    echo [ERROR] Nie znaleziono folderu backend.
    pause
    exit /b
)

REM Aktywuj �rodowisko wirtualne
call .\venv\Scripts\activate.bat || (
    echo [ERROR] Nie mo�na aktywowa� �rodowiska virtualenv.
    pause
    exit /b
)

REM Przejscie do katalogu z ktorego odpali sie uvicorn
cd /d C:\kalendarz_aplikacja\backend || (
    echo [ERROR] Nie znaleziono folderu backend.
    pause
    exit /b
)


REM Uruchom aplikacj� FastAPI przez uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 || (
    echo [ERROR] Nie uda�o si� uruchomi� uvicorn.
)

pause