import subprocess
import sys
import os

def get_task_name():
    return "NotionSafeBackup"

def get_script_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'run_backup.bat'))

def get_python_executable():
    # This function is no longer directly used for the task command,
    # but kept for consistency if needed elsewhere.
    python_executable = sys.executable
    if python_executable.endswith("python.exe"):
        return python_executable.replace("python.exe", "pythonw.exe")
    return python_executable

def create_task(interval_hours):
    task_name = get_task_name()
    script_path = get_script_path()
    
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
        "/tr", f'"{script_path}"',
        "/sc", schedule_type,
    ]
    if modifier:
        command.extend(["/mo", modifier])
    command.append("/f")
    
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        return (True, f"Task '{task_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        return (False, f"Error creating task: {e.stderr}")

def delete_task():
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
