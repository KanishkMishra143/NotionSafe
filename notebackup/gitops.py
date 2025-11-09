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
        if not os.path.exists(os.path.join(repo_path, ".git")):
            log.info(f"Initializing new Git repository at: {repo_path}")
            history_repo = git.Repo.init(repo_path)
        else:
            history_repo = git.Repo(repo_path)

        # Destination for snapshot inside the history repo
        snapshot_dest_in_repo = os.path.join(repo_path, os.path.basename(snapshot_folder))

        # Only copy if the source and destination are different
        if os.path.normpath(snapshot_folder) != os.path.normpath(snapshot_dest_in_repo):
            # Copy the snapshot folder into the history repo
            log.info(f"Copying {snapshot_folder} to {snapshot_dest_in_repo}")
            if os.path.exists(snapshot_dest_in_repo):
                shutil.rmtree(snapshot_dest_in_repo)
            shutil.copytree(snapshot_folder, snapshot_dest_in_repo)

        if 'history' not in history_repo.heads:
            log.info("Creating 'history' branch.")
            history_repo.git.checkout('-b', 'history')
        else:
            history_repo.git.checkout('history')

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
