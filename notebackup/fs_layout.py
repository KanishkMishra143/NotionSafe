import os
from datetime import datetime

def create_snapshot_dir(base_path):
    """
    Creates a timestamped directory for a new snapshot.
    e.g., /path/to/backups/2025-10-31_12-30-00
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    snapshot_path = os.path.join(base_path, timestamp)
    os.makedirs(snapshot_path, exist_ok=True)
    return snapshot_path

def update_latest_symlink(base_path, snapshot_path):
    """
    Creates or updates a 'latest' symlink to point to the most recent snapshot.
    """
    latest_link = os.path.join(base_path, "latest")
    if os.path.lexists(latest_link):
        os.remove(latest_link)
    os.symlink(os.path.basename(snapshot_path), latest_link)
    print(f"Updated 'latest' symlink to point to {os.path.basename(snapshot_path)}")
