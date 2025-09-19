@echo off
chcp 65001 >nul
echo ========================================
echo    Captcha Automation Launcher
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

:: Check if .env file exists
if not exist ".env" (
    echo ❌ .env file not found!
    echo Creating default .env file...
    copy /y ".env.example" ".env" >nul 2>&1
    echo Please edit .env file with your configuration
    notepad ".env"
    pause
    exit /b 1
)

:: Create virtual environment if not exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

:: Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Install Playwright browser
echo Installing Playwright browser...
python -m playwright install chromium

:: Run the application
echo.
echo ========================================
echo    Starting Captcha Automation
echo ========================================
echo.
python main.py

:: Pause to see the results
echo.
pause

:: Deactivate virtual environment
deactivate