import sys
import pytest
from unittest.mock import patch, MagicMock
from notebackup.exporter import export_cli

# Common arguments required by notion2md
ARGS = ["--token", "dummy_token", "--id", "dummy_id"]

# Test case for when notion2md is run as a subprocess
def test_export_cli_subprocess_fallback():
    with patch('subprocess.run') as mock_subprocess_run:
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        
        # Patch the callables directly to None to force fallback
        with patch('notebackup.exporter._export_callable', None):
            with patch('notebackup.exporter._main_callable', None):
                result = export_cli(ARGS)
                
                expected_cmd = [sys.executable, '-m', 'notion2md'] + ARGS
                mock_subprocess_run.assert_called_once_with(expected_cmd, check=False)
                assert result == 0

# Test case for when an in-process callable is found
def test_export_cli_in_process_callable():
    mock_callable = MagicMock(return_value=123)
    
    # Patch the _export_callable variable directly
    with patch('notebackup.exporter._export_callable', mock_callable):
        result = export_cli(ARGS)
        mock_callable.assert_called_once_with(ARGS)
        assert result == 123

# Test case for when __main__.main callable is found
def test_export_cli_main_callable():
    mock_main_callable = MagicMock(return_value=456)
    # Patch _export_callable to None and _main_callable directly
    with patch('notebackup.exporter._export_callable', None):
        with patch('notebackup.exporter._main_callable', mock_main_callable):
            result = export_cli(ARGS)
            mock_main_callable.assert_called_once_with(ARGS)
            assert result == 456

# Test case for when __main__.main callable expects argv style
def test_export_cli_main_callable_argv_style():
    mock_main_callable = MagicMock(side_effect=[TypeError, 789])
    # Patch _export_callable to None and _main_callable directly
    with patch('notebackup.exporter._export_callable', None):
        with patch('notebackup.exporter._main_callable', mock_main_callable):
            result = export_cli(ARGS)
            
            assert mock_main_callable.call_count == 2
            # The passthrough function retries with the same list, so both calls are identical
            mock_main_callable.assert_any_call(ARGS)
            assert result == 789
