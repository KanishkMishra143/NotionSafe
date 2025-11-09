import logging
import sys

def setup_logger():
    """Configures and returns a root logger for the application."""
    logger = logging.getLogger("notebackup")
    logger.setLevel(logging.INFO)

    logger.propagate = False

    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

log = setup_logger()
