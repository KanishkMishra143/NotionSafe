import pytest
from unittest.mock import patch, mock_open, call
import os
import yaml
from notebackup.cli import load_config, run_backup

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
MOCK_CONFIG = yaml.safe_load(MOCK_CONFIG_CONTENT)

@patch('os.path.exists', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data=MOCK_CONFIG_CONTENT)
@patch('yaml.safe_load', return_value=MOCK_CONFIG)
def test_load_config(mock_yaml_load, mock_open_file, mock_path_exists):
    """
    Test that the load_config function correctly reads and parses the configuration file.
    """
    config_path = "~/.noteback/test_config.yaml"
    config = load_config(config_path)

    expected_config_path = os.path.expanduser(config_path)
    mock_path_exists.assert_called_once_with(expected_config_path)
    mock_open_file.assert_called_once_with(expected_config_path, 'r')
    mock_yaml_load.assert_called_once()
    assert config == MOCK_CONFIG

@patch('notebackup.auth.get_notion_token', return_value="dummy_token")
@patch('notebackup.fs_layout.create_snapshot_dir', return_value="dummy/snapshot/path")
@patch('notebackup.exporter.export_cli')
@patch('notebackup.cli.get_page_title', side_effect=lambda notion, page_id: page_id)
@patch('notebackup.fs_layout.update_latest_marker')
@patch('notebackup.storage.rsync_to_external')
@patch('notebackup.gitops.perform_git_backup')
@patch('post_process.post_process_file')
@patch('notion_client.Client')
def test_run_backup_calls_exporter_with_correct_ids(mock_notion_client, mock_post_process, mock_gitops, mock_rsync, mock_update_marker, mock_get_title, mock_export_cli, mock_create_dir, mock_get_token):
    """
    Test that the run_backup function calls the exporter with the correct arguments.
    """
    run_backup(MOCK_CONFIG)

    assert mock_export_cli.call_count == 3

    expected_calls = [
        call(['--token', 'dummy_token', '--path', 'dummy/snapshot/path', '--unzipped', '--id', 'page1_id', '--name', 'page1_id']),
        call(['--token', 'dummy_token', '--path', 'dummy/snapshot/path', '--unzipped', '--id', 'page2_id', '--name', 'page2_id']),
        call(['--token', 'dummy_token', '--path', 'dummy/snapshot/path', '--unzipped', '--id', 'db1_id', '--name', 'db1_id'])
    ]
    mock_export_cli.assert_has_calls(expected_calls, any_order=True)
