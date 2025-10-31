#!/bin/bash
set -euo pipefail

# This script creates and enables a systemd user timer for NotionSafe.

# --- Configuration ---
SERVICE_NAME="notionsafe"
SERVICE_DESCRIPTION="NotionSafe Backup Runner"
TIMER_DESCRIPTION="Run NotionSafe backup daily"
# Run daily at 2:00 AM
TIMER_CALENDAR="*-*-* 02:00:00"
# ---

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )"
PYTHON_EXEC="${PROJECT_DIR}/venv/bin/python"
RUNNER_SCRIPT="${PROJECT_DIR}/scripts/backup_runner.py"
SYSTEMD_USER_DIR="${HOME}/.config/systemd/user"

mkdir -p "${SYSTEMD_USER_DIR}"

# --- Create systemd service file ---
SERVICE_FILE="${SYSTEMD_USER_DIR}/${SERVICE_NAME}.service"
echo "Creating service file at ${SERVICE_FILE}"

cat > "${SERVICE_FILE}" << EOL
[Unit]
Description=${SERVICE_DESCRIPTION}
After=network.target

[Service]
Type=oneshot
ExecStart=${PYTHON_EXEC} ${RUNNER_SCRIPT}
WorkingDirectory=${PROJECT_DIR}

[Install]
WantedBy=default.target
EOL

# --- Create systemd timer file ---
TIMER_FILE="${SYSTEMD_USER_DIR}/${SERVICE_NAME}.timer"
echo "Creating timer file at ${TIMER_FILE}"

cat > "${TIMER_FILE}" << EOL
[Unit]
Description=${TIMER_DESCRIPTION}

[Timer]
OnCalendar=${TIMER_CALENDAR}
Persistent=true

[Install]
WantedBy=timers.target
EOL

# --- Reload, enable, and start the timer ---
echo "Reloading systemd user daemon..."
systemctl --user daemon-reload

echo "Enabling and starting the timer..."
systemctl --user enable "${SERVICE_NAME}.timer"
systemctl --user start "${SERVICE_NAME}.timer"

echo "--- Success! ---"
echo "NotionSafe timer is now active."
echo "Check timer status with: systemctl --user list-timers"
echo "Check service logs with: journalctl --user -u ${SERVICE_NAME}.service"
