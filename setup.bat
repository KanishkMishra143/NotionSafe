@echo off
setlocal

echo.
echo --- NotionSafe Setup for Windows ---
echo.

:: --- 1. Check for Python ---
echo Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python is not found. Please install Python 3.10 or newer from python.org.
    echo Then, run this script again.
    echo.
    pause
    goto :eof
)
echo Python found.

:: --- 2. Setup Python Virtual Environment ---
echo.
echo Setting up Python virtual environment...
if not exist venv (
    python -m venv venv
    echo Created Python virtual environment in 'venv/'.
) else (
    echo Virtual environment 'venv/' already exists.
)

:: --- 3. Install Dependencies into the venv ---
echo.
echo Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip >nul
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies.
    pause
    goto :eof
)
echo Dependencies installed successfully.
deactivate

echo.
echo --- Setup Complete! ---
echo.
echo To run the application, please close this window and run 'run.bat'.
echo.
pause
endlocal