import subprocess
import sys
import os

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

def create_task(interval_hours):
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
