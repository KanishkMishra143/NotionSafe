import pytest
from unittest.mock import patch, MagicMock
from notebackup.scheduler import run_continuously

@patch('sys.exit')
@patch('time.sleep', side_effect=[None, KeyboardInterrupt])
@patch('schedule.every')
def test_run_continuously_schedules_job(mock_every, mock_sleep, mock_exit):
    """
    Test that run_continuously schedules the job correctly.
    """
    job_func = MagicMock()
    run_continuously(job_func, interval_hours=12)

    mock_every.assert_called_once_with(12)
    mock_every.return_value.hours.do.assert_called_once_with(job_func)
    mock_exit.assert_called_once_with(0)
