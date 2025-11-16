# notebackup/core.py

from notebackup import cli
from notebackup.cli import InvalidNotionTokenError
from notebackup.logger import log

class BackupRunner:
    """
    A UI-agnostic class to run the backup process.
    """
    def __init__(self, config_path):
        self.config_path = config_path

    def run(self, progress_callback=None, finished_callback=None, error_callback=None, invalid_token_callback=None):
        """
        Executes the backup process and uses callbacks to report status.

        :param progress_callback: A function to call with progress updates (int).
        :param finished_callback: A function to call on successful completion.
        :param error_callback: A function to call on a general error (receives exception string).
        :param invalid_token_callback: A function to call for an InvalidNotionTokenError.
        """
        try:
            cli.main(config_path=self.config_path, progress_callback=progress_callback)

            if finished_callback:
                finished_callback()

        except InvalidNotionTokenError:
            log.warning("Invalid Notion Token detected during backup.")
            if invalid_token_callback:
                invalid_token_callback()
        except Exception as e:
            log.error(f"An unexpected error occurred during backup: {e}", exc_info=True)
            if error_callback:
                error_callback(str(e))
