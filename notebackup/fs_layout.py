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

def update_latest_marker(base_path, snapshot_path):
    """
    Creates or updates a 'latest.txt' file to point to the most recent snapshot.
    The file will contain the absolute path to the snapshot.
    """
    latest_marker_file = os.path.join(base_path, "latest.txt")
    try:
        with open(latest_marker_file, "w") as f:
            f.write(snapshot_path)
        print(f"Updated 'latest.txt' to point to {snapshot_path}")
    except IOError as e:
        print(f"Error writing 'latest.txt' marker file: {e}")
