import subprocess
import sys
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# The project root is one level above the 'scripts' folder
project_root = os.path.abspath(os.path.join(script_dir, '..'))

# Define the path to pythonw.exe and the backup_runner.py script
pythonw_exe = os.path.join(project_root, "venv", "Scripts", "pythonw.exe")
backup_runner_script = os.path.join(script_dir, "backup_runner.py")

# Command to execute
command = [pythonw_exe, backup_runner_script]

# Use STARTUPINFO to hide the window
startupinfo = None
if sys.platform == "win32":
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE # This is the key

# Launch the process
try:
    # Popen is non-blocking, which is what we want for a launcher script
    subprocess.Popen(command, cwd=project_root, startupinfo=startupinfo,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except Exception as e:
    # Log any errors if this launcher fails
    with open(os.path.join(project_root, "launcher_error.log"), "a") as f:
        f.write(f"Error launching NotionSafe backup: {e}\n")
