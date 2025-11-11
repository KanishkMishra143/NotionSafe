import subprocess
import sys
import os
import platform

def get_task_name():
    return "NotionSafeBackup"

def get_py_script_path():
    """Gets the absolute path to the python backup runner script."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'backup_runner.py'))

def get_launcher_script_path():
    """Gets the absolute path to the python launcher script."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'launch_hidden.py'))

def get_python_executable():
    """
    Gets the path to the pythonw.exe executable within the same virtual environment.
    This ensures that the scheduled task runs without a console window.
    """
    python_executable = sys.executable
    # sys.executable could be python.exe or pythonw.exe. We want to be sure to use pythonw.exe
    # for the background task.
    if python_executable.endswith("python.exe"):
        pythonw_exe = python_executable.replace("python.exe", "pythonw.exe")
        if os.path.exists(pythonw_exe):
            return pythonw_exe
    # If it's already pythonw.exe or we can't find pythonw.exe, return the original.
    return python_executable

def create_task_linux_systemd(interval_hours):
    service_name = "notionsafe-backup.service"
    timer_name = "notionsafe-backup.timer"
    
    python_exe = sys.executable # Use the current Python executable
    script_path = get_py_script_path() # The script to run
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) # D:\notionsafe

    # Ensure the script path is executable
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
        # Write service file
        subprocess.run(["sudo", "tee", f"/etc/systemd/system/{service_name}"], input=service_content.encode(), check=True, capture_output=True)
        # Write timer file
        subprocess.run(["sudo", "tee", f"/etc/systemd/system/{timer_name}"], input=timer_content.encode(), check=True, capture_output=True)

        # Reload systemd, enable and start timer
        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True, capture_output=True)
        subprocess.run(["sudo", "systemctl", "enable", timer_name], check=True, capture_output=True)
        subprocess.run(["sudo", "systemctl", "start", timer_name], check=True, capture_output=True)

        return (True, f"Systemd timer '{timer_name}' created and started successfully.")
    except subprocess.CalledProcessError as e:
        return (False, f"Error creating systemd task: {e.stderr.decode()}")
    except Exception as e:
        return (False, f"An unexpected error occurred: {e}")

def delete_task_linux_systemd():
    service_name = "notionsafe-backup.service"
    timer_name = "notionsafe-backup.timer"

    try:
        # Stop and disable timer and service
        subprocess.run(["sudo", "systemctl", "stop", timer_name], check=False, capture_output=True)
        subprocess.run(["sudo", "systemctl", "disable", timer_name], check=False, capture_output=True)
        subprocess.run(["sudo", "systemctl", "stop", service_name], check=False, capture_output=True)
        subprocess.run(["sudo", "systemctl", "disable", service_name], check=False, capture_output=True)

        # Delete files
        subprocess.run(["sudo", "rm", "-f", f"/etc/systemd/system/{timer_name}"], check=False, capture_output=True)
        subprocess.run(["sudo", "rm", "-f", f"/etc/systemd/system/{service_name}"], check=False, capture_output=True)

        # Reload systemd
        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True, capture_output=True)

        return (True, f"Systemd timer '{timer_name}' deleted successfully.")
    except subprocess.CalledProcessError as e:
        return (False, f"Error deleting systemd task: {e.stderr.decode()}")
    except Exception as e:
        return (False, f"An unexpected error occurred: {e}")

def create_task(interval_hours):
    if platform.system() == "Windows":
        task_name = get_task_name()
        launcher_script_path = get_launcher_script_path()
        python_exe = get_python_executable()
        
        # Execute pythonw.exe with the launcher script.
        # The launcher script will then use subprocess.Popen with SW_HIDE to run the backup.
        task_command = f'"{python_exe}" "{launcher_script_path}"'

        if interval_hours >= 24:
            schedule_type = "DAILY"
            modifier = str(int(interval_hours / 24))
        elif interval_hours >= 1:
            schedule_type = "HOURLY"
            modifier = str(int(interval_hours))
        else:
            interval_minutes = int(interval_hours * 60)
            if interval_minutes == 0:
                interval_minutes = 1 # Run at least every minute
            schedule_type = "MINUTE"
            modifier = str(interval_minutes)

        command = [
            "schtasks", "/create",
            "/tn", task_name,
            "/tr", task_command,
            "/sc", schedule_type,
        ]
        if modifier:
            command.extend(["/mo", modifier])
        command.extend(["/ru", "SYSTEM", "/rl", "HIGHEST"]) # Run as SYSTEM, highest privileges
        command.append("/f")
        
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            return (True, f"Task '{task_name}' created successfully.")
        except subprocess.CalledProcessError as e:
            return (False, f"Error creating task: {e.stderr}")
    elif platform.system() == "Linux":
        return create_task_linux_systemd(interval_hours)
    else:
        return (False, "Unsupported operating system.")

def delete_task():
    if platform.system() == "Windows":
        task_name = get_task_name()
        
        command = [
            "schtasks", "/delete",
            "/tn", task_name,
            "/f"
        ]
        
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            return (True, f"Task '{task_name}' deleted successfully.")
        except subprocess.CalledProcessError as e:
            return (False, f"Error deleting task: {e.stderr}")
    elif platform.system() == "Linux":
        return delete_task_linux_systemd()
    else:
        return (False, "Unsupported operating system.")
