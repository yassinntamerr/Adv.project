@echo off
REM Face Recognition System - Command Line Interface
REM This script starts the face recognition system on Windows

echo.
echo ================================================
echo   STUDENT FACE RECOGNITION SYSTEM
echo   Advanced Statistics Project
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import deepface" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Dependencies not installed
    echo Running setup...
    python setup.py
    if %errorlevel% neq 0 (
        echo [ERROR] Setup failed
        pause
        exit /b 1
    )
)

REM Check if CSV exists
if not exist StudentPicsDataset.csv (
    echo [ERROR] StudentPicsDataset.csv not found!
    echo Please place the CSV file in this directory
    pause
    exit /b 1
)

REM Run main application
echo.
echo [INFO] Starting Face Recognition System...
echo [INFO] Press Ctrl+C to stop
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application failed
    pause
)
