import pytest
from unittest.mock import patch, MagicMock
import git
from notebackup.gitops import perform_git_backup

@pytest.fixture
def temp_repo_setup(tmp_path):
    """Create a temporary directory structure for git tests."""
    repo_path = tmp_path / "repo"
    snapshot_folder = tmp_path / "snapshot"
    repo_path.mkdir()
    snapshot_folder.mkdir()
    (snapshot_folder / "test.md").write_text("test content")
    return str(repo_path), str(snapshot_folder)

@patch('notebackup.gitops.shutil.move')
@patch('notebackup.gitops.git.Repo.clone_from')
@patch('notebackup.gitops.git.Repo', autospec=True)
@patch('notebackup.gitops.shutil.copytree')
@patch('notebackup.gitops.tempfile.TemporaryDirectory')
def test_perform_git_backup_new_repo(mock_tempdir, mock_copytree, mock_repo_class, mock_clone_from, mock_move, temp_repo_setup, tmp_path):
    """
    Test the full git backup process for a new repository.
    """
    repo_path, snapshot_folder = temp_repo_setup
    
    # --- Mock setup ---
    master_repo_path = tmp_path / "master_repo"
    master_repo_path.mkdir()
    mock_tempdir.return_value.__enter__.return_value = str(master_repo_path)

    # Simulate clone failing for an empty repo
    mock_clone_from.side_effect = git.exc.GitCommandError("clone", "empty repository")

    # History repo mocks
    mock_history_repo = MagicMock()
    mock_history_repo.heads = []
    mock_history_repo.is_dirty.return_value = True
    # Simulate checkout failure to test the 'except' block
    mock_history_repo.git.checkout.side_effect = [
        git.exc.GitCommandError("checkout", "branch not found"),
        None  # Success for the second call
    ]
    
    # Remotes need to be iterable and indexable
    mock_history_remotes = MagicMock()
    mock_history_remotes.__iter__.return_value = iter([]) # No remotes initially
    mock_history_repo.remotes = mock_history_remotes

    # Master repo mocks
    mock_master_repo = MagicMock()
    mock_master_remotes = MagicMock()
    mock_master_repo.remotes = mock_master_remotes

    # Make Repo class return the correct mock
    mock_repo_class.init.side_effect = [mock_history_repo, mock_master_repo]

    # --- Act ---
    perform_git_backup(repo_path, snapshot_folder, "origin", "https://example.com/repo.git")

    # --- Assertions ---
    from unittest.mock import call

    # Assert clone was attempted
    mock_clone_from.assert_called_once()

    # History Branch (asserting fallback to init)
    mock_repo_class.init.assert_any_call(repo_path)
    
    # Assert that checkout was attempted first for 'history', then with '-b history'
    calls = [call('history'), call('-b', 'history')]
    mock_history_repo.git.checkout.assert_has_calls(calls)

    mock_history_repo.git.add.assert_called_once()
    mock_history_repo.index.commit.assert_called_once()
    mock_history_repo.create_remote.assert_called_once_with("origin", "https://example.com/repo.git")
    mock_history_remotes.__getitem__.assert_called_with('origin')
    mock_history_remotes.__getitem__().push.assert_called_once_with(refspec='history:history')

    # Master Branch
    mock_repo_class.init.assert_any_call(str(master_repo_path))
    mock_master_repo.git.add.assert_called_once_with(A=True)
    mock_master_repo.index.commit.assert_called_once()
    mock_master_repo.create_remote.assert_called_once_with("origin", "https://example.com/repo.git")
    mock_master_remotes.__getitem__.assert_called_with('origin')
    mock_master_remotes.__getitem__().push.assert_called_once_with(refspec='HEAD:master', force=True)
