import subprocess
import os

def install_systemd_timer():
    """
    Installs and enables a systemd user timer for the backup script.
    """
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'install_systemd_timer.sh'))
    if not os.path.exists(script_path):
        print(f"Error: Systemd install script not found at {script_path}")
        return

    print("Running systemd timer installation script...")
    try:
        subprocess.run(["bash", script_path], check=True)
        print("Systemd timer installed and started successfully.")
        print("You can check the status with: systemctl --user status notionsafe.timer")
    except subprocess.CalledProcessError as e:
        print(f"Error installing systemd timer: {e}")
    except FileNotFoundError:
        print("Error: 'bash' command not found. Please ensure you are on a Linux system.")

def add_cron_job():
    """
    Provides instructions for adding a cron job.
    """
    runner_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'backup_runner.py'))
    python_executable = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'venv', 'bin', 'python'))
    
    print("\n--- Cron Job Instructions ---")
    print("To run the backup daily at 2 AM, add the following line to your crontab.")
    print("Run 'crontab -e' and add:")
    print(f"0 2 * * * {python_executable} {runner_script_path}")
    print("---------------------------\n")
