@echo off
echo ========================================
echo Installing Cassava Disease Detection App
echo ========================================
echo.

echo Step 1: Installing Backend Dependencies...
echo.
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Backend installation failed!
    echo Please check if Python and pip are installed correctly.
    pause
    exit /b 1
)

echo.
echo Step 2: Installing Frontend Dependencies...
echo.
cd ..\frontend
call npm install
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Frontend installation failed!
    echo Please check if Node.js and npm are installed correctly.
    pause
    exit /b 1
)

cd ..

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To start the application, run: START_APP.bat
echo Or follow the instructions in SETUP_GUIDE.md
echo.
pause
