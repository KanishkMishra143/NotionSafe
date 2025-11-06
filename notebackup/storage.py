import subprocess
import os
import shutil
from notebackup.gitops import commit_and_push

# def rsync_to_external(source_path, dest_path):
#     """
#     Uses rsync to copy the snapshot to an external drive.
#     """
#     if not os.path.exists(dest_path):
#         os.makedirs(dest_path)
    
#     cmd = ["rsync", "-avh", "--delete", f"{source_path}/", dest_path]
#     print(f"Running rsync command: {' '.join(cmd)}")
#     try:
#         subprocess.run(cmd, check=True, capture_output=True, text=True)
#         print("Rsync to external drive completed successfully.")
#     except subprocess.CalledProcessError as e:
#         print(f"Error during rsync: {e.stderr}")

def rsync_to_external(source_path, dest_path):
    """
    Copies the snapshot to an external drive using shutil.
    Mimics rsync's --delete by removing the destination first.
    """
    # Construct the full destination path including the timestamped folder name
    final_dest_path = os.path.join(dest_path, os.path.basename(source_path))

    print(f"Copying from {source_path} to {final_dest_path}")
    try:
        if os.path.exists(final_dest_path): # Check for the final destination path
            shutil.rmtree(final_dest_path)
            print(f"Removed existing destination directory: {final_dest_path}")
        shutil.copytree(source_path, final_dest_path) # Copy to the final destination path
        print("Copy to external drive completed successfully.")
    except Exception as e:
        print(f"Error during copy to external drive: {e}")

# def git_commit(repo_path, snapshot_folder, remote_name, remote_url):
#     """
#     Commits the new snapshot to the git repository.
#     """
#     script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'git_commit_update.sh'))
#     cmd = ["bash", script_path, repo_path, snapshot_folder, remote_name, remote_url]
#     print(f"Running git commit script: {' '.join(cmd)}")
#     try:
#         subprocess.run(cmd, check=True, capture_output=True, text=True)
#         print("Git commit and push completed successfully.")
#     except subprocess.CalledProcessError as e:
#         print(f"Error during git operations: {e.stderr}")

def git_commit(repo_path, snapshot_folder, remote_name, remote_url):
    """
    Commits the new snapshot to the git repository using GitPython.
    """
    print(f"Committing snapshot {snapshot_folder} to git repository at {repo_path}")
    commit_message = f"NotionSafe backup: {snapshot_folder}"
    commit_and_push(repo_path, commit_message, remote_name, remote_url)
