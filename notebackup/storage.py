import subprocess
import os
import shutil

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