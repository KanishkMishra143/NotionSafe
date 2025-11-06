import pytest
from unittest.mock import patch, mock_open, MagicMock, call
import sys
import os
import yaml

# tests/conftest.py
import gettext
import builtins
from types import SimpleNamespace
import pytest

@pytest.fixture(autouse=True)
def disable_gettext_translation(monkeypatch):
    """
    Replace gettext.translation(...) with a dummy object that provides
    .gettext and .ngettext methods accepting str input and returning str.
    This avoids mock_open vs bytes issues in tests.
    autouse=True => applied to every test automatically (safe).
    """
    class DummyTranslation:
        def gettext(self, msg):
            # identity function: returns message unchanged
            return msg
        def ngettext(self, msg1, msg2, n):
            return msg1 if n == 1 else msg2

    # monkeypatch gettext.translation to return DummyTranslation()
    monkeypatch.setattr(gettext, "translation", lambda *args, **kwargs: DummyTranslation())
    # also patch gettext.gettext global function (optional but safe)
    monkeypatch.setattr(gettext, "_", lambda s: s, raising=False)

    yield
    # after test, monkeypatch fixture will restore originals



# Mock configuration content for testing
MOCK_CONFIG_CONTENT = """
notion:
  page_ids: ["page1_id", "page2_id"]
  database_ids: ["db1_id"]
storage:
  local_path: "~/notebackups"
  external_drive:
    enabled: false
  git:
    enabled: false
"""

@pytest.fixture
def mock_cli_env():
  """
  A pytest fixture that mocks the environment for CLI tests.
  It patches sys.argv, os.path.exists, builtins.open, yaml.safe_load,
  and all the notebackup modules that are called by cli.main().
  It yields a dictionary of the mocks so that tests can access them.
  """
  test_args = ["cli.py", "--config", "~/.noteback/test_config.yaml"]
  with patch.object(sys, 'argv', test_args), \
    patch('os.path.exists', return_value=True), \
    patch('builtins.open', mock_open(read_data=MOCK_CONFIG_CONTENT)) as mock_file, \
    patch('yaml.safe_load', return_value=yaml.safe_load(MOCK_CONFIG_CONTENT)) as mock_yaml_load, \
    patch('notebackup.auth.get_notion_token', return_value="dummy_token"), \
    patch('notebackup.fs_layout.create_snapshot_dir', return_value="dummy/snapshot/path") as mock_create_dir, \
    patch('notebackup.fs_layout.update_latest_marker') as mock_update_marker, \
    patch('notebackup.exporter.export_cli') as mock_export_cli, \
    patch('notebackup.storage.rsync_to_external') as mock_rsync, \
    patch('notebackup.storage.git_commit') as mock_git_commit:
      
      yield {
        "mock_file": mock_file,
        "mock_yaml_load": mock_yaml_load,
        "mock_create_dir": mock_create_dir,
        "mock_update_marker": mock_update_marker,
        "mock_export_cli": mock_export_cli,
        "mock_rsync": mock_rsync,
        "mock_git_commit": mock_git_commit,
      }

def test_cli_main_reads_config_file(mock_cli_env):
    # # Mock sys.argv to simulate command-line arguments
    # test_args = ["cli.py", "--config", "~/.noteback/test_config.yaml"]
    # with patch.object(sys, 'argv', test_args):
    #     # Mock os.path.exists to pretend the config file exists
    #     with patch('os.path.exists', return_value=True):
    #         # Mock open to return our dummy config content
    #         with patch('builtins.open', mock_open(read_data=MOCK_CONFIG_CONTENT)) as mock_file:
    #             # Mock yaml.safe_load to ensure it's called and returns parsed data
    #             with patch('yaml.safe_load', return_value=yaml.safe_load(MOCK_CONFIG_CONTENT)) as mock_yaml_load:
    #                 # Mock auth.get_notion_token to prevent actual token retrieval
    #                 with patch('notebackup.auth.get_notion_token', return_value="dummy_token"):
    #                     # Mock other external calls that main() might make
    #                     with patch('notebackup.fs_layout.create_snapshot_dir'):
    #                         with patch('notebackup.fs_layout.update_latest_symlink'):
    #                             with patch('notebackup.exporter.export_cli'):
    #                                 with patch('notebackup.storage.rsync_to_external'):
    #                                     with patch('notebackup.storage.git_commit'):

                                            #Impot and call the main function 
                                            from notebackup.cli import main
                                            main()

                                            # Assertions
                                            # Check if open was called with the correct path
                                            expected_config_path = os.path.expanduser("~/.noteback/test_config.yaml")
                                            mock_cli_env["mock_file"].assert_called_once_with(expected_config_path, 'r')
                                            
                                            # Check if yaml.safe_load was called
                                            mock_cli_env["mock_yaml_load"].assert_called_once()

def test_cli_main_calls_exporter_with_correct_ids(mock_cli_env):
    # # Mock sys.argv to simulate command-line arguments
    # test_args = ["cli.py", "--config", "~/.noteback/test_config.yaml"]
    # with patch.object(sys, 'argv', test_args):
    #     # Mock os.path.exists to pretend the config file exists
    #     with patch('os.path.exists', return_value=True):
    #         # Mock open to return our dummy config content
    #         with patch('builtins.open', mock_open(read_data=MOCK_CONFIG_CONTENT)):
    #             # Mock yaml.safe_load to ensure it's called and returns parsed data
    #             with patch('yaml.safe_load', return_value=yaml.safe_load(MOCK_CONFIG_CONTENT)):
    #                 # Mock auth.get_notion_token to prevent actual token retrieval
    #                 with patch('notebackup.auth.get_notion_token', return_value="dummy_token"):
    #                     # Mock auth.get_notion_token to prevent actual token retrieval
    #                     with patch('notebackup.auth.get_notion_token', return_value="dummy_token"):
    #                         # Mock other external calls that main() might make
    #                         with patch('notebackup.fs_layout.create_snapshot_dir', return_value="dummy/snapshot/path") as mock_crate_dir:
    #                             with patch('notebackup.fs_layout.update_latest_symlink'):
    #                                 with patch('notebackup.exporter.export_cli') as mock_export_cli:
    #                                     with patch('notebackup.storage.rsync_to_external'):
    #                                         with patch('notebackup.storage.git_commit'):
                                                from notebackup.cli import main
                                                main()

                                                # Assertions
                                                # Check that export_cli was called for pages and databases
                                                assert mock_cli_env["mock_export_cli"].call_count == 3

                                                # Check the arguments for each call
                                                expected_calls = [call(['--token', 'dummy_token', '--path', 'dummy/snapshot/path', '--id', 'page1_id']), call(['--token', 'dummy_token', '--path', 'dummy/snapshot/path', '--id', 'page2_id']), call(['--token', 'dummy_token', '--path', 'dummy/snapshot/path', '--id', 'db1_id'])]
                                                mock_cli_env["mock_export_cli"].assert_has_calls(expected_calls, any_order=True)
