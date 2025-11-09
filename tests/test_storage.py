import pytest
from unittest.mock import patch, call
import os
import shutil
from notebackup.storage import rsync_to_external
 
def test_rsync_to_external_copies_files_and_deletes_existing(tmp_path):
    source_path = tmp_path / "source"
    dest_path = tmp_path / "destination"
   
    # Create dummy source directory and file
    source_path.mkdir()
    (source_path / "file.txt").write_text("test content")
   
    # Create dummy destination directory (to be deleted)
    dest_path.mkdir()
    (dest_path / "old_file.txt").write_text("old content")
   
    with patch('os.path.exists', return_value=True), \
        patch('shutil.rmtree') as mock_rmtree, \
        patch('shutil.copytree') as mock_copytree:
  
        rsync_to_external(str(source_path), str(dest_path))
  
        # Assertions
        final_dest_path = os.path.join(dest_path, os.path.basename(source_path))
        mock_rmtree.assert_called_once_with(str(final_dest_path))
        mock_copytree.assert_called_once_with(str(source_path), str(final_dest_path))