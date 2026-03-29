import os
import sys
import logging
import traceback
import getpass
import tempfile

# --- Set up dedicated logging for the service ---
log_dir = os.path.join(tempfile.gettempdir(), "notionsafe")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "service.log")

# Configure file logging
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Get the root logger and add the file handler
# This ensures that any module using logging will also write to this file
root_logger = logging.getLogger()
root_logger.addHandler(file_handler)
root_logger.setLevel(logging.INFO)

# --- Main script logic ---
def main():
    """
    Entry point for the background scheduler service.
    Loads the configuration and runs the backup process once.
    """
    try:
        root_logger.info("--- Scheduler service triggered ---")
        root_logger.info(f"Current User: {getpass.getuser()}")
        root_logger.info(f"Current Working Directory: {os.getcwd()}")
        root_logger.info(f"Python Executable: {sys.executable}")
        
        # Add the project root to the Python path to allow for absolute imports
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        root_logger.info(f"Project Root: {project_root}")
        root_logger.info(f"Sys Path: {sys.path}")

        from notebackup import cli

        config_path = os.path.expanduser("~/.noteback/config.yaml")
        root_logger.info(f"Attempting to load config from: {config_path}")
        
        if not os.path.exists(config_path):
            root_logger.error("Configuration file not found. The service cannot run without configuration.")
            # Try to find config in SYSTEM user's profile if running as SYSTEM
            if getpass.getuser().upper() == "SYSTEM":
                system_profile_config = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "System32", "config", "systemprofile", ".noteback", "config.yaml")
                root_logger.info(f"Running as SYSTEM, checking for config at: {system_profile_config}")
                if os.path.exists(system_profile_config):
                    config_path = system_profile_config
                    root_logger.info("Found config in SYSTEM profile.")
                else:
                    root_logger.error("Config file not found in SYSTEM profile either. Exiting.")
                    return

        cli.main(config_path=config_path)
        root_logger.info("--- Scheduler service backup run completed successfully ---")

    except Exception as e:
        root_logger.error("--- Scheduler service backup run failed ---")
        root_logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()