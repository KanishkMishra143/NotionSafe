import time
import schedule
from PySide6.QtCore import QThread, Signal
import datetime

class SchedulerThread(QThread):
    """
    A QThread that runs a scheduled job in the background.
    """
    status_changed = Signal(str)
    error = Signal(str)
    next_run_time = Signal(str)
    job_started = Signal()
    job_finished = Signal()
    progress = Signal(int)

    def __init__(self, job_func, interval_hours=24, config_path='~/.noteback/config.yaml'):
        super().__init__()
        self.job_func = job_func
        self.interval_hours = interval_hours
        self.config_path = config_path
        self.running = False

    def run(self):
        """
        Runs the scheduler loop.
        """
        self.running = True
        self.status_changed.emit(f"Scheduler started. Next run in {self.interval_hours} hours.")

        schedule.every(self.interval_hours).hours.do(self.job_wrapper)

        while self.running:
            schedule.run_pending()
            next_run = schedule.next_run() # Call next_run as a function
            if next_run:
                self.next_run_time.emit(next_run.strftime("%Y-%m-%d %H:%M:%S"))
            else:
                self.next_run_time.emit("Not scheduled") # Emit a default message if no next run
            time.sleep(1)

        self.status_changed.emit("Scheduler stopped.")

    def job_wrapper(self):
        """
        Wrapper around the job function to handle errors.
        """
        try:
            self.job_started.emit()
            self.status_changed.emit("Backup job started...")
            self.job_func(self.config_path, progress_callback=self.progress)
            self.status_changed.emit(f"Backup job finished. Next run in {self.interval_hours} hours.")
            self.job_finished.emit()
        except Exception as e:
            self.error.emit(f"Error during backup: {e}")

    def stop(self):
        """
        Stops the scheduler loop.
        """
        self.running = False
