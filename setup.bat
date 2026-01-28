@echo off
REM Setup script for Chemical Equipment Parameter Visualizer (Windows)

echo =========================================
echo Chemical Equipment Parameter Visualizer
echo Setup Script (Windows)
echo =========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo Python is required but not installed. Aborting.
    exit /b 1
)

REM Check Node.js version
echo Checking Node.js version...
node --version
if errorlevel 1 (
    echo Node.js is required but not installed. Aborting.
    exit /b 1
)

REM Setup Backend
echo.
echo Setting up Django Backend...
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
echo.
echo Creating superuser for authentication...
echo Please enter username, email, and password when prompted:
python manage.py createsuperuser
cd ..

REM Setup Frontend
echo.
echo Setting up React Frontend...
cd frontend
call npm install
cd ..

REM Setup Desktop
echo.
echo Setting up Desktop Application...
cd desktop
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt
cd ..

echo.
echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo To start the application:
echo.
echo 1. Start Django Backend (Command Prompt 1):
echo    cd backend
echo    venv\Scripts\activate
echo    python manage.py runserver
echo.
echo 2. Start React Frontend (Command Prompt 2):
echo    cd frontend
echo    npm start
echo.
echo 3. Start Desktop App (Command Prompt 3):
echo    cd desktop
echo    venv\Scripts\activate
echo    python main.py
echo.
echo Web app will be available at: http://localhost:3000
echo API will be available at: http://localhost:8000
echo.
pause
