#!/usr/bin/env python3
import sys
import os
import time
import yaml

# Add the project root to the Python path to allow for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from notebackup import cli, scheduler

def backup_job():
    """
    Defines the job to be executed by the scheduler.
    This function calls the main backup logic from the notebackup CLI module.
    """
    print(f"--- [{time.ctime()}] Starting scheduled backup ---")
    try:
        # We call cli.main() without arguments to run a standard backup.
        # The argparse in cli.main() will use the default config file.
        cli.main()
        print(f"--- [{time.ctime()}] Finished scheduled backup successfully ---")
    except Exception as e:
        print(f"--- [{time.ctime()}] An error occurred during the backup job: {e} ---")

if __name__ == "__main__":
    # Load configuration to get the backup frequency
    config_path = os.path.expanduser("~/.noteback/config.yaml")
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found at {config_path}")
        print("Please run the configuration script first: python scripts/configure.py")
        sys.exit(1)

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Get the backup interval from the config, with a fallback to 24 hours
    backup_interval_hours = config.get('storage', {}).get('backup_frequency_hours', 24)
    
    # This will start the infinite loop for the scheduler.
    scheduler.run_continuously(backup_job, interval_hours=backup_interval_hours)