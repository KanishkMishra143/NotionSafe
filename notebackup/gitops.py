import git
import os

def init_repo(repo_path):
    """Initializes a new Git repository if one doesn't exist."""
    if not os.path.exists(os.path.join(repo_path, ".git")):
        print(f"No Git repository found at {repo_path}, initializing a new one.")
        repo = git.Repo.init(repo_path)
        print(f"Initialized empty Git repository in {repo_path}")
        return repo
    return git.Repo(repo_path)

def has_remote(repo, remote_name):
    """Checks if a remote with the given name exists."""
    return remote_name in [r.name for r in repo.remotes]

def check_for_changes(repo):
    """Check if there are any uncommitted changes."""
    return repo.is_dirty(untracked_files=True)

def perform_git_backup(repo_path, snapshot_folder, remote_name, remote_url):
    """
    Orchestrates the entire git backup process.
    Initializes repo, adds all changes, commits, and pushes to the remote.
    """
    try:
        repo = init_repo(repo_path)

        # Check for changes before proceeding
        if not check_for_changes(repo):
            print("No changes detected in the backup. Git backup skipped.")
            return

        print("Changes detected, proceeding with Git backup.")
        repo.git.add(A=True)
        
        commit_message = f"NotionSafe backup: {os.path.basename(snapshot_folder)}"
        repo.index.commit(commit_message)
        print(f"Successfully committed changes with message: '{commit_message}'")

        # Handle remote repository
        if not has_remote(repo, remote_name):
            print(f"Remote '{remote_name}' not found. Creating it with URL: {remote_url}")
            repo.create_remote(remote_name, remote_url)
        
        print(f"Pushing changes to remote '{remote_name}'...")
        repo.remotes[remote_name].push(refspec='HEAD')
        print("Git push to remote successful.")

    except git.exc.GitCommandError as e:
        print(f"An error occurred during Git operation: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")