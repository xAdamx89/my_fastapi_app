@echo off
REM PrzejdŸ do katalogu, gdzie jest venv
cd /d C:\kalendarz_aplikacja || (
    echo [ERROR] Nie znaleziono folderu backend.
    pause
    exit /b
)

REM Aktywuj œrodowisko wirtualne
call .\venv\Scripts\activate.bat || (
    echo [ERROR] Nie mo¿na aktywowaæ œrodowiska virtualenv.
    pause
    exit /b
)

REM Przejscie do katalogu z ktorego odpali sie uvicorn
cd /d C:\kalendarz_aplikacja\backend || (
    echo [ERROR] Nie znaleziono folderu backend.
    pause
    exit /b
)


REM Uruchom aplikacjê FastAPI przez uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 || (
    echo [ERROR] Nie uda³o siê uruchomiæ uvicorn.
)

pause