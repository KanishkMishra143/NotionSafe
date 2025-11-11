import pytest
from unittest.mock import MagicMock, patch
from notebackup.scheduler import SchedulerThread
import time

@pytest.fixture
def scheduler_thread():
    """
    Provides a SchedulerThread instance for testing.
    """
    job_func = MagicMock()
    thread = SchedulerThread(job_func=job_func, interval_hours=1)
    yield thread
    # Ensure the thread is stopped after the test
    if thread.isRunning():
        thread.stop()
        thread.wait()

def test_scheduler_thread_init(scheduler_thread):
    """
    Test the initialization of the SchedulerThread.
    """
    assert not scheduler_thread.running
    assert scheduler_thread.interval_hours == 1

@patch('schedule.every')
@patch('schedule.run_pending')
def test_scheduler_thread_run_and_stop(mock_run_pending, mock_every, scheduler_thread):
    """
    Test the run and stop methods of the SchedulerThread by directly calling run().
    """
    mock_status_slot = MagicMock()
    scheduler_thread.status_changed.connect(mock_status_slot)

    # Use a side effect to stop the loop after one iteration
    def stop_loop_side_effect(*args):
        scheduler_thread.running = False

    with patch('time.sleep', side_effect=stop_loop_side_effect):
        scheduler_thread.run() # Directly call run()

    # Assertions
    assert not scheduler_thread.running
    mock_every.assert_called_once_with(1)
    mock_every.return_value.hours.do.assert_called_once_with(scheduler_thread.job_wrapper)
    mock_run_pending.assert_called_once() # Should be called once before the loop stops
    
    mock_status_slot.assert_any_call("Scheduler started. Next run in 1 hours.")
    mock_status_slot.assert_called_with("Scheduler stopped.")

def test_job_wrapper_success(scheduler_thread):
    """
    Test the job_wrapper method for a successful job execution.
    """
    mock_status_slot = MagicMock()
    scheduler_thread.status_changed.connect(mock_status_slot)

    scheduler_thread.job_wrapper()

    scheduler_thread.job_func.assert_called_once_with(scheduler_thread.config_path)
    mock_status_slot.assert_any_call("Backup job started...")
    mock_status_slot.assert_called_with("Backup job finished. Next run in 1 hours.")

def test_job_wrapper_error(scheduler_thread):
    """
    Test the job_wrapper method when the job raises an exception.
    """
    error_message = "Test Error"
    scheduler_thread.job_func.side_effect = Exception(error_message)
    mock_error_slot = MagicMock()
    scheduler_thread.error.connect(mock_error_slot)

    scheduler_thread.job_wrapper()

    mock_error_slot.assert_called_once_with(f"Error during backup: {error_message}")