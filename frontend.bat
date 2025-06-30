@echo off

REM PrzejdŸ do katalogu z venv
cd /d C:\kalendarz_aplikacja || (
    echo [ERROR] Nie znaleziono folderu z venv.
    pause
    exit /b
)

REM Aktywuj œrodowisko virtualenv
call venv\Scripts\activate.bat || (
    echo [ERROR] Nie mo¿na aktywowaæ œrodowiska virtualenv.
    pause
    exit /b
)

REM PrzejdŸ do frontend
cd /d C:\kalendarz_aplikacja\frontend

REM Uruchom frontend przez npx vite --host
npx vite --host

REM Pauza na koñcu
pause