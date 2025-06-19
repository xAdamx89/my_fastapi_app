@echo off   

::Aktywacja środowiska python
call venv\Scripts\activate.bat

::backend
cd backend\app
start /b uvicorn app:app --reload

cd ..\..

::frontend
cd frontend
start /b npm run dev

echo Serwery uruchomione. Naciśnij dowolny klawisz, aby zakończyć...
pause >nul