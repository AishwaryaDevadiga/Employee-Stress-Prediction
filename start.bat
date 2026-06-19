@echo off
REM Employee Stress Prediction - Easy Launcher
REM This script starts the API and opens the web dashboard

cls
echo.
echo ========================================
echo  Employee Stress Prediction Dashboard
echo ========================================
echo.
echo Starting Flask API Server...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start Flask app
python app.py
