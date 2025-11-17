import git
import os
import shutil
import tempfile
from .logger import log

# =====================================================================================
# NON-DESTRUCTIVE PHILOSOPHY
#
# This module is designed to be non-destructive. It operates on git repositories
# in a way that preserves history and prevents accidental data loss.
#
# Key principles:
# 1. Temporary Directories: New backups are prepared in a temporary location
#    outside the git working directory to ensure git operations start from a
#    clean state, preventing accidental commits of partial or unrelated files.
# 2. Explicit Branch Handling:
#    - 'history' branch: A linear, append-only history of all backups is
#      maintained. Rebase is used instead of merge to keep the history clean.
#    - 'master' branch: Contains ONLY the latest backup. It is force-pushed
#      to reflect the most recent state without accumulating history.
# 3. Safety First: Operations that could be destructive (like cleaning the
#    directory for the master branch) are carefully scoped to the git repo path.
#
# DO NOT REMOVE THIS COMMENT. This philosophy is central to the design and
# safety of the NotionSafe backup process. Future modifications must adhere
# to these principles.
# =====================================================================================

def _get_repo(repo_path, remote_url, remote_name="origin"):
    """
    Initializes or opens a Git repository, ensuring it's cloned and configured.
    """
    if os.path.exists(os.path.join(repo_path, ".git")):
        log.info(f"Found existing Git repository at: {repo_path}")
        repo = git.Repo(repo_path)
    else:
        log.info(f"Local git repo not found. Cloning from {remote_url} into {repo_path}.")
        os.makedirs(repo_path, exist_ok=True)
        try:
            # Clone to a temporary directory first
            with tempfile.TemporaryDirectory() as temp_clone_path:
                log.info(f"Cloning into temporary directory: {temp_clone_path}")
                git.Repo.clone_from(remote_url, temp_clone_path)
                
                # Move the .git directory to the final destination
                git_dir = os.path.join(temp_clone_path, ".git")
                dest_git_dir = os.path.join(repo_path, ".git")
                log.info(f"Moving .git directory to {dest_git_dir}")
                shutil.move(git_dir, dest_git_dir)

            # Now, open the repository from the correct path
            repo = git.Repo(repo_path)
            log.info("Successfully initialized repository from remote.")
        except git.exc.GitCommandError as e:
            if "empty repository" in str(e).lower():
                log.warning(f"Cloning failed as remote is empty. Initializing a new repository at: {repo_path}")
                repo = git.Repo.init(repo_path)
            else:
                log.error(f"Failed to clone repository: {e}", exc_info=True)
                raise
    
    # Ensure remote is configured
    if remote_name not in [r.name for r in repo.remotes]:
        repo.create_remote(remote_name, remote_url)
    else:
        repo.remotes[remote_name].set_url(remote_url)
        
    return repo

def _handle_history_branch(repo, snapshot_folder, remote_name):
    """
    Handles the 'history' branch logic: checkout, copy, commit, and push.
    """
    log.info("--- Handling History Branch ---")
    history_branch = 'history'
    
    # Clean working directory before checkout
    if repo.is_dirty(untracked_files=True):
        log.warning("Working directory is dirty. Stashing changes.")
        repo.git.stash('save', '--include-untracked')

    try:
        # Fetch latest changes from remote history branch
        if remote_name in [r.name for r in repo.remotes] and f"{remote_name}/{history_branch}" in repo.git.branch('-r'):
            log.info(f"Fetching latest from remote '{history_branch}' branch.")
            repo.remotes[remote_name].fetch()
    except git.exc.GitCommandError as e:
        log.warning(f"Could not fetch from remote. It might not exist yet. Error: {e}")

    try:
        log.info(f"Checking out '{history_branch}' branch.")
        repo.git.checkout(history_branch)
    except git.exc.GitCommandError:
        log.info(f"'{history_branch}' branch not found, creating new orphan branch.")
        repo.git.checkout('--orphan', history_branch)
        repo.git.rm('-rf', '.') # Clear the branch to start fresh

    # Pull with rebase to avoid merge conflicts on the linear history
    try:
        log.info(f"Pulling with rebase from remote '{history_branch}'.")
        repo.git.pull(remote_name, history_branch, "--rebase")
    except git.exc.GitCommandError as e:
        if "couldn't find remote ref" in str(e).lower() or "no tracking information" in str(e).lower():
            log.info(f"No remote '{history_branch}' branch to pull from. Will push as a new branch.")
        else:
            log.error(f"Failed to pull from remote '{history_branch}': {e}", exc_info=True)
            raise # Re-raise critical pull errors
            
    # Copy snapshot into the history repo
    snapshot_dest = os.path.join(repo.working_dir, os.path.basename(snapshot_folder))
    log.info(f"Copying snapshot to {snapshot_dest}")
    if os.path.exists(snapshot_dest):
        shutil.rmtree(snapshot_dest)
    shutil.copytree(snapshot_folder, snapshot_dest)

    # Commit and Push
    if repo.is_dirty(untracked_files=True):
        log.info(f"Adding snapshot '{os.path.basename(snapshot_folder)}' to history branch.")
        repo.git.add(snapshot_dest)
        commit_message = f"feat: Add snapshot {os.path.basename(snapshot_folder)}"
        repo.index.commit(commit_message)
        log.info(f"Committed to history branch: '{commit_message}'")
        
        log.info(f"Pushing history branch to remote '{remote_name}'...")
        repo.remotes[remote_name].push(refspec=f'{history_branch}:{history_branch}')
    else:
        log.info("No changes to commit in history branch.")

def _handle_master_branch(repo, snapshot_folder, remote_name):
    """
    Handles the 'master' branch logic: checkout, clean, copy, commit, and force-push.
    """
    log.info("--- Handling Master Branch ---")
    master_branch = 'master'

    try:
        log.info(f"Checking out '{master_branch}' branch.")
        repo.git.checkout(master_branch)
    except git.exc.GitCommandError:
        log.info(f"'{master_branch}' branch not found, creating new orphan branch.")
        repo.git.checkout('--orphan', master_branch)

    # Clean the working directory completely
    log.info("Cleaning working directory for master branch update.")
    # List all files and directories except .git and remove them
    for item in os.listdir(repo.working_dir):
        if item == '.git':
            continue
        path = os.path.join(repo.working_dir, item)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except Exception as e:
            log.error(f"Failed to remove {path}: {e}")


    # Copy snapshot contents to the repo's root
    log.info("Copying latest backup to the root of the master branch.")
    for item in os.listdir(snapshot_folder):
        src = os.path.join(snapshot_folder, item)
        dest = os.path.join(repo.working_dir, item)
        if os.path.isdir(src):
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)

    # Commit and Force Push
    repo.git.add(A=True)
    try:
        commit_message = f"feat: Update to latest backup {os.path.basename(snapshot_folder)}"
        repo.index.commit(commit_message)
        log.info(f"Committed latest backup to master branch: '{commit_message}'")
        
        log.info(f"Force pushing master branch to remote '{remote_name}'...")
        repo.remotes[remote_name].push(refspec=f'HEAD:{master_branch}', force=True)
    except git.exc.GitCommandError as e:
        if "nothing to commit" in str(e) or "no changes added to commit" in str(e):
            log.info("No changes to commit in master branch.")
        else:
            raise # Re-raise other git errors


def perform_git_backup(repo_path, snapshot_folder, remote_name, remote_url):
    """
    Orchestrates a git backup process for 'history' and 'master' branches.
    """
    repo = None
    try:
        repo_path = os.path.normpath(repo_path)
        snapshot_folder = os.path.normpath(snapshot_folder)

        with tempfile.TemporaryDirectory() as temp_dir:
            # Move the new snapshot to a safe temporary location
            temp_snapshot_path = os.path.join(temp_dir, os.path.basename(snapshot_folder))
            log.info(f"Temporarily moving snapshot to {temp_snapshot_path}")
            shutil.move(snapshot_folder, temp_snapshot_path)

            # Now the git working directory is clean.
            repo = _get_repo(repo_path, remote_url, remote_name)

            # --- History Branch ---
            _handle_history_branch(repo, temp_snapshot_path, remote_name)

            # --- Master Branch ---
            _handle_master_branch(repo, temp_snapshot_path, remote_name)

        log.info("Git backup process completed successfully.")

    except git.exc.GitCommandError as e:
        error_str = str(e).lower()
        if "permission denied" in error_str or "could not read from remote repository" in error_str:
            log.error("Git push failed due to an authentication error.")
            log.error(f"The URL being used is: {remote_url}")
            log.error("Please verify your credentials (SSH key or Personal Access Token) and permissions for the repository.")
        else:
            log.error(f"An error occurred during Git operation: {e}", exc_info=True)
        raise  # Re-raise the exception to propagate the failure
    except Exception as e:
        log.error(f"An unexpected error occurred during the Git backup: {e}", exc_info=True)
        raise  # Re-raise the exception to propagate the failure
    finally:
        if repo:
            repo.close()
