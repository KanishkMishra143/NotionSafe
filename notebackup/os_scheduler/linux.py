# notebackup/os_scheduler/linux.py

import subprocess
import sys
import os

def get_py_script_path():
    """Gets the absolute path to the python backup runner script."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'backup_runner.py'))

def create(interval_hours):
    service_name = "notionsafe-backup.service"
    timer_name = "notionsafe-backup.timer"
    
    python_exe = sys.executable
    script_path = get_py_script_path()
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    os.chmod(script_path, 0o755)

    # Service file is simpler: no need for [Install] as it's triggered by the timer.
    service_content = f"""[Unit]
Description=NotionSafe Backup Service
After=network.target

[Service]
Type=oneshot
ExecStart={python_exe} {script_path}
WorkingDirectory={project_root}
StandardOutput=journal
StandardError=journal
User={os.getlogin()}
"""

    # --- Robust Calendar String Generation ---
    try:
        interval_hours = float(interval_hours)
        if interval_hours <= 0:
            interval_hours = 24  # Default for non-positive values
    except (ValueError, TypeError):
        interval_hours = 24  # Default for non-numeric values

    calendar_string = ""
    # Use is_integer() to check for whole numbers, even if they are floats (e.g., 6.0)
    if interval_hours.is_integer():
        interval_int = int(interval_hours)
        if interval_int >= 24:
            calendar_string = "daily"
        elif interval_int >= 1:
            # Every N hours (where N is an integer)
            hours = ",".join(str(h) for h in range(0, 24, interval_int))
            calendar_string = f"{hours}:00:00"
        else: # This case should not be hit due to the <= 0 check above, but as a fallback
             interval_minutes = round(interval_hours * 60)
             if interval_minutes >= 1:
                calendar_string = f"*:0/{interval_minutes}"  # Every N minutes
             else:
                calendar_string = "*:0/1" # Default to every minute if interval is too small
    else:  # Sub-hour or non-integer hour interval
        interval_minutes = round(interval_hours * 60)
        if interval_minutes >= 1:
            calendar_string = f"*:0/{interval_minutes}"  # Every N minutes
        else:
            # Interval is less than a minute, default to every minute.
            calendar_string = "*:0/1"


    timer_content = f"""[Unit]
Description=Runs NotionSafe backup on a schedule

[Timer]
OnCalendar={calendar_string}
Persistent=true
Unit={service_name}

[Install]
WantedBy=timers.target
"""

    # Consolidate all commands into a single string to be run with pkexec
    command_str = f"""
set -e
cat <<EOF > /etc/systemd/system/{service_name}
{service_content}
EOF

cat <<EOF > /etc/systemd/system/{timer_name}
{timer_content}
EOF

systemctl daemon-reload
systemctl enable {timer_name}
systemctl start {timer_name}
"""
    try:
        # Use pkexec to get a graphical password prompt
        subprocess.run(
            ["pkexec", "sh", "-c", command_str],
            check=True, 
            capture_output=True
        )
        return (True, f"Systemd timer '{timer_name}' created and started successfully.")
    except subprocess.CalledProcessError as e:
        error_detail = e.stderr.decode() if e.stderr else "No error detail."
        if "authentication failed" in error_detail.lower():
            return (False, "Authentication failed. Could not create the scheduled task.")
        return (False, f"Error creating systemd task: {error_detail}")
    except FileNotFoundError:
        return (False, "Error: 'pkexec' command not found. Please ensure Polkit is installed on your system.")
    except Exception as e:
        return (False, f"An unexpected error occurred: {e}")

def delete():
    service_name = "notionsafe-backup.service"
    timer_name = "notionsafe-backup.timer"

    # Consolidate all commands. Ignore errors for stop/disable in case they aren't running.
    command_str = f"""
set -e
systemctl stop {timer_name} >/dev/null 2>&1 || true
systemctl disable {timer_name} >/dev/null 2>&1 || true
rm -f /etc/systemd/system/{timer_name}
rm -f /etc/systemd/system/{service_name}
systemctl daemon-reload
"""
    try:
        # Use pkexec to get a graphical password prompt
        subprocess.run(
            ["pkexec", "sh", "-c", command_str],
            check=True, 
            capture_output=True
        )
        return (True, f"Systemd timer '{timer_name}' deleted successfully.")
    except subprocess.CalledProcessError as e:
        error_detail = e.stderr.decode() if e.stderr else "No error detail."
        if "authentication failed" in error_detail.lower():
            return (False, "Authentication failed. Could not delete the scheduled task.")
        return (False, f"Error deleting systemd task: {error_detail}")
    except FileNotFoundError:
        return (False, "Error: 'pkexec' command not found. Please ensure Polkit is installed on your system.")
    except Exception as e:
        return (False, f"An unexpected error occurred: {e}")

def is_scheduled():
    timer_name = "notionsafe-backup.timer"
    try:
        # No sudo/pkexec needed for read-only status check
        result = subprocess.run(["systemctl", "is-enabled", timer_name], capture_output=True, text=True)
        return result.returncode == 0 and "enabled" in result.stdout.strip()
    except Exception:
        return False
