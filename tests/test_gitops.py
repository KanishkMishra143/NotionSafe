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

@patch('notebackup.gitops.git.Repo.clone_from')
@patch('notebackup.gitops.git.Repo', autospec=True)
@patch('notebackup.gitops.tempfile.TemporaryDirectory')
def test_perform_git_backup_new_repo(mock_tempdir, mock_repo_class, mock_clone_from, temp_repo_setup, tmp_path):
    """
    Test the full git backup process for a new repository, using real filesystem
    operations within a temporary directory.
    """
    repo_path, snapshot_folder = temp_repo_setup
    
    # --- Mock setup ---
    # Provide a real directory for the TemporaryDirectory context manager
    temp_dir_path = tmp_path / "temp_dir"
    temp_dir_path.mkdir()
    mock_tempdir.return_value.__enter__.return_value = str(temp_dir_path)

    # Simulate clone failing for an empty repo, triggering init
    mock_clone_from.side_effect = git.exc.GitCommandError("clone", "empty repository")

    # A single mock repo is used for all git operations
    mock_repo = MagicMock()
    mock_repo.is_dirty.return_value = True
    
    # Provide a real working directory for the mock repo
    real_working_dir = tmp_path / "real_repo_workdir"
    real_working_dir.mkdir()
    # Create a dummy .git file to satisfy the cleaning logic in _handle_master_branch
    (real_working_dir / ".git").touch()
    mock_repo.working_dir = str(real_working_dir)

    # Simulate checkout failures to test orphan branch creation
    mock_repo.git.checkout.side_effect = [
        git.exc.GitCommandError("checkout", "branch 'history' not found"),
        None,
        git.exc.GitCommandError("checkout", "branch 'master' not found"),
        None,
    ]
    
    # Mock remotes
    mock_remotes = MagicMock()
    mock_remotes.__iter__.return_value = iter([])
    mock_repo.remotes = mock_remotes
    
    # When Repo is initialized, it returns our single mock_repo
    mock_repo_class.init.return_value = mock_repo

    # --- Act ---
    perform_git_backup(repo_path, snapshot_folder, "origin", "https://example.com/repo.git")

    # --- Assertions ---
    from unittest.mock import call

    # Assert clone was attempted, then fell back to init
    mock_clone_from.assert_called_once()
    mock_repo_class.init.assert_called_once_with(repo_path)
    
    # Assert checkout sequence for both branches
    checkout_calls = [
        call('history'), 
        call('--orphan', 'history'),
        call('master'),
        call('--orphan', 'master')
    ]
    mock_repo.git.checkout.assert_has_calls(checkout_calls)

    # Assert history branch operations
    mock_repo.git.pull.assert_called_once_with('origin', 'history', '--rebase')
    
    # Assert master branch operations
    mock_repo.git.add.assert_any_call(A=True)

    # Assert commits and pushes
    commit_calls = mock_repo.index.commit.call_count
    assert commit_calls == 2, f"Expected 2 commits, but got {commit_calls}"

    push_calls = mock_remotes.__getitem__().push.call_count
    assert push_calls == 2, f"Expected 2 pushes, but got {push_calls}"
    mock_remotes.__getitem__().push.assert_any_call(refspec='history:history')
    mock_remotes.__getitem__().push.assert_any_call(refspec='HEAD:master', force=True)
