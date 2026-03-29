#!/bin/bash

# This script installs the NotionSafe backup scheduler as a systemd user service.

set -e

# --- Configuration ---
SERVICE_NAME="notionsafe"
SERVICE_FILE="$SERVICE_NAME.service"
TIMER_FILE="$SERVICE_NAME.timer"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PYTHON="$PROJECT_ROOT/venv/bin/python"
SCHEDULER_SCRIPT="$SCRIPT_DIR/run_scheduler_service.py"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

# --- Validation ---
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Python executable not found at $VENV_PYTHON"
    echo "Please ensure the virtual environment is set up correctly."
    exit 1
fi

if [ ! -f "$SCHEDULER_SCRIPT" ]; then
    echo "Error: Scheduler script not found at $SCHEDULER_SCRIPT"
    exit 1
fi

# --- Service File ---
echo "Creating systemd service file..."
cat > "$SERVICE_FILE" << EOL
[Unit]
Description=NotionSafe Backup Job
Wants=$TIMER_FILE

[Service]
Type=oneshot
ExecStart=$VENV_PYTHON $SCHEDULER_SCRIPT
EOL

# --- Timer File ---
echo "Creating systemd timer file..."
cat > "$TIMER_FILE" << EOL
[Unit]
Description=Run NotionSafe backup daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
EOL

# --- Installation ---
echo "Installing systemd user files..."
mkdir -p "$SYSTEMD_USER_DIR"
mv "$SERVICE_FILE" "$SYSTEMD_USER_DIR/"
mv "$TIMER_FILE" "$SYSTEMD_USER_DIR/"

# --- Systemd Control ---
echo "Reloading systemd user daemon and enabling timer..."
systemctl --user daemon-reload
systemctl --user enable --now "$TIMER_FILE"

echo "Successfully installed and started the NotionSafe systemd timer."
echo "Your backups will now run daily."
echo "To check the status, run: systemctl --user status $TIMER_FILE"
