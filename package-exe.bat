@echo off
setlocal

echo . 
echo --- Packaging NotionSafe for Windows ---
echo .

:: Build the executable without prompting the user for confirmation
echo Building using PyInstaller
pyinstaller --noconfirm NotionSafe.spec
if %errorlevel% neq 0 (
    echo PyInstaller build failed!
    exit /b %errorlevel%
)

:: Zip the output directory
echo .
echo  Zipping the output...
if exist "dist\NotionSafe-Windows.zip" del "dist\NotionSafe-Windows.zip"

:: Use powershell to zip the folder cleanly
powershell -Command "Compress-Archive -Path 'dist\NotionSafe' -DestinationPath 'release\NotionSafe-Windows.zip' -Force"

if %errorlevel% neq 0 (
    echo Zipping failed!
    exit /b %errorlevel%
)

echo.
echo --- Packaging complete. The zipped release is located at: release\NotionSafe-Windows.zip ---
echo.
endlocal