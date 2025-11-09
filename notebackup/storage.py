import os
import shutil
from .logger import log

def rsync_to_external(source_path, dest_path):
    """
    Copies the snapshot to an external drive using shutil.
    Mimics rsync's --delete by removing the destination first.
    """
    final_dest_path = os.path.join(dest_path, os.path.basename(source_path))

    log.info(f"Copying from {source_path} to {final_dest_path}")
    try:
        if os.path.exists(final_dest_path):
            shutil.rmtree(final_dest_path)
            log.info(f"Removed existing destination directory: {final_dest_path}")
        shutil.copytree(source_path, final_dest_path)
        log.info("Copy to external drive completed successfully.")
    except Exception as e:
        log.error(f"Error during copy to external drive: {e}", exc_info=True)
