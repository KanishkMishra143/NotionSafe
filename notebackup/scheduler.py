import time
import schedule
import sys

def run_continuously(job_func, interval_hours=24):
    """
    Runs a job at a specified interval using in-process scheduling.

    This function will run in an infinite loop.

    :param job_func: The function to execute at each interval.
    :param interval_hours: The interval in hours between job executions.
    """
    print(f"Scheduling job to run every {interval_hours} hours.")
    schedule.every(interval_hours).hours.do(job_func)

    print("Scheduler started. Press Ctrl+C to stop.")
    try:
        while True:
            schedule.run_pending()
            # Sleep for a short duration to avoid busy-waiting
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")
        sys.exit(0)