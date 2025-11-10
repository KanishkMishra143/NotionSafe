import git
import os
import shutil
import tempfile
from .logger import log

def perform_git_backup(repo_path, snapshot_folder, remote_name, remote_url):
    """
    Orchestrates a sophisticated git backup process using a main repo for history 
    and a temporary repo for the master branch.
    """
    try:
        # Normalize paths
        repo_path = os.path.normpath(repo_path)
        snapshot_folder = os.path.normpath(snapshot_folder)

        # --- History Branch --- 
        log.info("--- Handling History Branch ---")
        history_repo = None
        if os.path.exists(os.path.join(repo_path, ".git")):
            log.info(f"Found existing Git repository at: {repo_path}")
            history_repo = git.Repo(repo_path)
        else:
            log.info(f"Local git repo not found. Initializing by cloning from {remote_url} into a temporary directory.")
            with tempfile.TemporaryDirectory() as temp_clone_dir:
                try:
                    # Clone into a temporary empty directory
                    git.Repo.clone_from(remote_url, temp_clone_dir)
                    log.info("Successfully cloned repository to temporary location.")
                    # Move the .git directory to the actual repo_path
                    shutil.move(os.path.join(temp_clone_dir, ".git"), os.path.join(repo_path, ".git"))
                    log.info(f"Moved .git directory to {repo_path}")
                    history_repo = git.Repo(repo_path)
                except git.exc.GitCommandError as e:
                    if "empty repository" in str(e).lower() or "does not appear to be a git repository" in str(e).lower():
                        log.warning(f"Cloning failed, remote is likely empty. Initializing a new repository at: {repo_path}")
                        history_repo = git.Repo.init(repo_path)
                    else:
                        log.error(f"Failed to clone repository: {e}", exc_info=True)
                        raise

        if not history_repo:
            log.error("Fatal: Could not initialize or clone the git repository. Aborting git backup.")
            return

        # Destination for snapshot inside the history repo
        snapshot_dest_in_repo = os.path.join(repo_path, os.path.basename(snapshot_folder))

        # Only copy if the source and destination are different
        if os.path.normpath(snapshot_folder) != os.path.normpath(snapshot_dest_in_repo):
            # Copy the snapshot folder into the history repo
            log.info(f"Copying {snapshot_folder} to {snapshot_dest_in_repo}")
            if os.path.exists(snapshot_dest_in_repo):
                shutil.rmtree(snapshot_dest_in_repo)
            shutil.copytree(snapshot_folder, snapshot_dest_in_repo)

        try:
            log.info("Checking out 'history' branch.")
            history_repo.git.checkout('history')
        except git.exc.GitCommandError:
            log.info("'history' branch not found, creating new branch.")
            history_repo.git.checkout('-b', 'history')

        log.info(f"Adding snapshot {os.path.basename(snapshot_folder)} to history branch.")
        history_repo.git.add(snapshot_dest_in_repo)
        if history_repo.is_dirty(untracked_files=True):
            commit_message = f"feat: Add snapshot {os.path.basename(snapshot_folder)}"
            history_repo.index.commit(commit_message)
            log.info(f"Committed snapshot to history branch with message: '{commit_message}'")

        if remote_name not in [r.name for r in history_repo.remotes]:
            # Ensure the remote URL is up-to-date
            history_repo.create_remote(remote_name, remote_url)
        else:
            history_repo.remotes[remote_name].set_url(remote_url)
        
        log.info(f"Pushing history branch to remote '{remote_name}'...")
        history_repo.remotes[remote_name].push(refspec='history:history')

        # --- Master Branch (in temporary repo) ---
        log.info("--- Handling Master Branch ---")
        with tempfile.TemporaryDirectory() as temp_dir:
            log.info(f"Created temporary directory for master branch: {temp_dir}")
            master_repo = git.Repo.init(temp_dir)

            # Copy snapshot contents to the temp repo
            for item in os.listdir(snapshot_folder):
                s = os.path.join(snapshot_folder, item)
                d = os.path.join(temp_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, symlinks=True)
                else:
                    shutil.copy2(s, d)

            master_repo.git.add(A=True)
            commit_message = f"feat: Update to latest backup {os.path.basename(snapshot_folder)}"
            master_repo.index.commit(commit_message)
            log.info(f"Committed latest backup to master branch with message: '{commit_message}'")

            master_repo.create_remote(remote_name, remote_url)

            log.info(f"Force pushing master branch to remote '{remote_name}'...")
            master_repo.remotes[remote_name].push(refspec='HEAD:master', force=True)

            master_repo.close()

        log.info("Git backup process completed successfully.")

    except git.exc.GitCommandError as e:
        error_str = str(e).lower()
        if "permission denied" in error_str or "could not read from remote repository" in error_str:
            log.error("Git push failed due to an authentication error.")
            log.error(f"The URL being used is: {remote_url}")
            log.error("Please verify your credentials (SSH key or Personal Access Token) and permissions for the repository.")
        else:
            log.error(f"An error occurred during Git operation: {e}", exc_info=True)
    except Exception as e:
        log.error(f"An unexpected error occurred during the Git backup: {e}", exc_info=True)
