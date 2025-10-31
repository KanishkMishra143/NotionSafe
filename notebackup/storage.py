import subprocess
import os

def rsync_to_external(source_path, dest_path):
    """
    Uses rsync to copy the snapshot to an external drive.
    """
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    
    cmd = ["rsync", "-avh", "--delete", f"{source_path}/", dest_path]
    print(f"Running rsync command: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Rsync to external drive completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during rsync: {e.stderr}")

def git_commit(repo_path, snapshot_folder, remote_name, remote_url):
    """
    Commits the new snapshot to the git repository.
    """
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'git_commit_update.sh'))
    cmd = ["bash", script_path, repo_path, snapshot_folder, remote_name, remote_url]
    print(f"Running git commit script: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Git commit and push completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during git operations: {e.stderr}")
