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
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

    os.chmod(script_path, 0o755)

    service_content = f"""
[Unit]
Description=NotionSafe Daily Backup Service
After=network.target

[Service]
Type=oneshot
ExecStart={python_exe} {script_path}
WorkingDirectory={project_root}
StandardOutput=journal
StandardError=journal
User={os.getlogin()}
Group={os.getlogin()}

[Install]
WantedBy=timers.target
"""

    timer_content = f"""
[Unit]
Description=Runs NotionSafe daily backup
Requires={service_name}

[Timer]
OnBootSec=1min
OnUnitActiveSec={interval_hours}h
Unit={service_name}

[Install]
WantedBy=timers.target
"""
    try:
        subprocess.run(["sudo", "tee", f"/etc/systemd/system/{service_name}"], input=service_content.encode(), check=True, capture_output=True)
        subprocess.run(["sudo", "tee", f"/etc/systemd/system/{timer_name}"], input=timer_content.encode(), check=True, capture_output=True)
        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True, capture_output=True)
        subprocess.run(["sudo", "systemctl", "enable", timer_name], check=True, capture_output=True)
        subprocess.run(["sudo", "systemctl", "start", timer_name], check=True, capture_output=True)
        return (True, f"Systemd timer '{timer_name}' created and started successfully.")
    except subprocess.CalledProcessError as e:
        return (False, f"Error creating systemd task: {e.stderr.decode()}")
    except Exception as e:
        return (False, f"An unexpected error occurred: {e}")

def delete():
    service_name = "notionsafe-backup.service"
    timer_name = "notionsafe-backup.timer"

    try:
        subprocess.run(["sudo", "systemctl", "stop", timer_name], check=False, capture_output=True)
        subprocess.run(["sudo", "systemctl", "disable", timer_name], check=False, capture_output=True)
        subprocess.run(["sudo", "systemctl", "stop", service_name], check=False, capture_output=True)
        subprocess.run(["sudo", "systemctl", "disable", service_name], check=False, capture_output=True)
        subprocess.run(["sudo", "rm", "-f", f"/etc/systemd/system/{timer_name}"], check=False, capture_output=True)
        subprocess.run(["sudo", "rm", "-f", f"/etc/systemd/system/{service_name}"], check=False, capture_output=True)
        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True, capture_output=True)
        return (True, f"Systemd timer '{timer_name}' deleted successfully.")
    except subprocess.CalledProcessError as e:
        return (False, f"Error deleting systemd task: {e.stderr.decode()}")
    except Exception as e:
        return (False, f"An unexpected error occurred: {e}")

def is_scheduled():
    timer_name = "notionsafe-backup.timer"
    try:
        result = subprocess.run(["systemctl", "is-enabled", timer_name], capture_output=True, text=True)
        return result.returncode == 0 and "enabled" in result.stdout.strip()
    except Exception:
        return False
