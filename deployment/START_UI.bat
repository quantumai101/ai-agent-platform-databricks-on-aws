@echo off
REM AI Agent Platform - Windows Launcher
REM Double-click this file to start the deployment UI

echo =====================================================
echo AI AGENT PLATFORM - ONE-CLICK DEPLOYMENT
echo =====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Checking for required files...

REM Check if index.html exists
if not exist "index.html" (
    echo ERROR: index.html not found!
    echo Please make sure index.html is in the same folder.
    echo.
    pause
    exit /b 1
)

echo Starting deployment UI...
echo.
echo Browser will open automatically at http://localhost:3000
echo Press Ctrl+C to stop the server
echo.

REM Start the Python server
python launch_ui.py

pause
