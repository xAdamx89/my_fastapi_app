@echo off
setlocal

:: Aktywacja środowiska virtualenv
echo Aktywacja środowiska Python...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Błąd: Nie można aktywować środowiska wirtualnego.
    pause
    exit /b 1
)

:: Uruchomienie backendu
echo Uruchamianie backendu...
cd backend/app/
start "Backend (FastAPI)" uvicorn backend_app:app --reload

:: Powrót do katalogu głównego
cd ..\..

:: Uruchomienie frontend (React)
echo Uruchamianie frontend...
cd frontend
start "Frontend (React)" /b npm run dev

:: Informacja dla użytkownika
echo -----------------------------------------------
echo Serwery uruchomione.
echo Backend: http://127.0.0.1:8000/docs
echo Frontend: http://localhost:5173
echo -----------------------------------------------
echo Naciśnij dowolny klawisz, aby zakończyć okno...
pause >nul