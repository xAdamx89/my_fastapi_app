@echo off
REM Przejdź do folderu projektu (jeśli potrzebne, ale jesteś już w nim)
cd /d "C:\Projekt zaliczeniowy - Programowanie w językach skryptowych\ma_fastapi_app"

REM Aktywuj środowisko wirtualne
call venv\Scripts\activate.bat

REM Uruchom backend FastAPI (uvicorn) w nowym oknie
start uvicorn backend.app.main:app --reload

REM Przejdź do frontend i uruchom npm run dev (w tym samym oknie)
cd frontend
npm run dev

REM Aby okno nie zamykało się od razu (opcjonalne)
pause