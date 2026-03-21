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

echo .
echo --- Asking if I want to make a release or not ---
echo .

set /p choice="Do you want to upload to GitHub now? (y/n): "
if /i "%choice%"=="y" (
    set /p tag="Enter version tag (e.g. v1.0.0): "
    gh release create %tag% .\release\NotionSafe-Windows.zip --generate-notes --latest
)

echo .
echo --- We are done ---
echo .
endlocal