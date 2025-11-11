#!/usr/bin/env python3
import sys
import os
import time
import yaml
import logging

# Add the project root to the Python path to allow for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from notebackup import cli

# Setup logging
log_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backup_runner.log'))
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def backup_job():
    """
    Defines the job to be executed by the scheduler.
    This function calls the main backup logic from the notebackup CLI module.
    """
    logging.info(f"--- [{time.ctime()}] Starting scheduled backup ---")
    try:
        # We call cli.main() without arguments to run a standard backup.
        # The argparse in cli.main() will use the default config file.
        if cli.main():
            logging.info(f"--- [{time.ctime()}] Finished scheduled backup successfully ---")
        else:
            logging.error(f"--- [{time.ctime()}] Finished scheduled backup with errors ---")
    except Exception as e:
        logging.error(f"--- [{time.ctime()}] An error occurred during the backup job: {e} ---", exc_info=True)

def main():
    logging.info("backup_runner.py main() started.")
    # Load configuration to get the backup frequency
    config_path = os.path.expanduser("~/.noteback/config.yaml")
    if not os.path.exists(config_path):
        logging.error(f"Error: Configuration file not found at {config_path}")
        logging.error("Please run the configuration script first: python scripts/configure.py")
        sys.exit(1)

    backup_job()
    logging.info("backup_runner.py main() finished.")

if __name__ == "__main__":
    main()