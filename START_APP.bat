@echo off
echo ========================================
echo Cassava Disease Detection Application
echo ========================================
echo.
echo Starting Backend Server...
echo.

cd backend
start cmd /k "python run.py"

timeout /t 5 /nobreak > nul

echo.
echo Starting Frontend Server...
echo.

cd ..\frontend
start cmd /k "npm start"

echo.
echo ========================================
echo Both servers are starting!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo ========================================
echo.
echo Press any key to exit this window...
pause > nul
