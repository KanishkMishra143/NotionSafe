import pytest
from unittest.mock import patch, MagicMock
from notebackup.gitops import commit_and_push

@patch('notebackup.gitops.init_repo')
@patch('notebackup.gitops.check_for_changes')
@patch('notebackup.gitops.has_remote', return_value=False) # Assume remote does not exist initially
def test_commit_and_push_with_changes(mock_has_remote, mock_check_for_changes, mock_init_repo, tmp_path):
    # Arrange
    repo_path = str(tmp_path / "test_repo")
    commit_message = "Test commit"
    remote_name = "origin"
    remote_url = "https://github.com/user/repo.git"

    mock_repo = MagicMock()
    mock_init_repo.return_value = mock_repo
    mock_check_for_changes.return_value = True

    # Mock the remote handling
    mock_remote = MagicMock()
    mock_repo.remotes = MagicMock()
    mock_repo.remotes.__getitem__.return_value = mock_remote

    # Act
    commit_and_push(repo_path, commit_message, remote_name, remote_url)

    # Assert
    mock_init_repo.assert_called_once_with(repo_path)
    mock_check_for_changes.assert_called_once_with(mock_repo)
    mock_repo.git.add.assert_called_once_with(A=True)
    mock_repo.index.commit.assert_called_once_with(commit_message)
    mock_repo.create_remote.assert_called_once_with(remote_name, remote_url)
    mock_remote.push.assert_called_once()

@patch('notebackup.gitops.init_repo')
@patch('notebackup.gitops.check_for_changes')
def test_commit_and_push_no_changes(mock_check_for_changes, mock_init_repo, tmp_path):
    # Arrange
    repo_path = str(tmp_path / "test_repo")
    commit_message = "Test commit"
    remote_name = "origin"
    remote_url = "https://github.com/user/repo.git"

    mock_repo = MagicMock()
    mock_init_repo.return_value = mock_repo
    mock_check_for_changes.return_value = False

    # Act
    commit_and_push(repo_path, commit_message, remote_name, remote_url)

    # Assert
    mock_init_repo.assert_called_once_with(repo_path)
    mock_check_for_changes.assert_called_once_with(mock_repo)
    mock_repo.git.add.assert_not_called()
    mock_repo.index.commit.assert_not_called()
