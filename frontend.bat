@echo off

REM Przejd� do katalogu z venv
cd /d C:\kalendarz_aplikacja || (
    echo [ERROR] Nie znaleziono folderu z venv.
    pause
    exit /b
)

REM Aktywuj �rodowisko virtualenv
call venv\Scripts\activate.bat || (
    echo [ERROR] Nie mo�na aktywowa� �rodowiska virtualenv.
    pause
    exit /b
)

REM Przejd� do frontend
cd /d C:\kalendarz_aplikacja\frontend

REM Uruchom frontend przez npx vite --host
npx vite --host

REM Pauza na ko�cu
pause