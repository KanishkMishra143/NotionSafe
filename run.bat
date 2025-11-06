@echo off
setlocal
echo Launching NotionSafe Environment...

:: This will open a new command prompt with the venv activated.
cmd /k "call venv\Scripts\activate.bat && title NotionSafe Environment && prompt (venv) $P$G"

endlocal