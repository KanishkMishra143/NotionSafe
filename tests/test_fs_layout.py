import os
from notebackup.fs_layout import create_snapshot_dir, update_latest_marker
from datetime import datetime

def test_create_snapshot_dir(tmp_path):
    """
    Test that a timestamped snapshot directory is created correctly.
    """
    base_path = tmp_path
    snapshot_path = create_snapshot_dir(str(base_path))

    assert os.path.isdir(snapshot_path)
    
    dir_name = os.path.basename(snapshot_path)
    current_year = str(datetime.now().year)
    assert dir_name.startswith(current_year)

def test_update_latest_marker(tmp_path):
    """
    Test that the latest.txt marker file is created and updated correctly.
    """
    base_path = tmp_path
    snapshot_path = os.path.join(str(base_path), "2025-01-01_12-00-00")
    os.makedirs(snapshot_path)

    update_latest_marker(str(base_path), snapshot_path)

    latest_txt_path = os.path.join(str(base_path), "latest.txt")
    assert os.path.isfile(latest_txt_path)

    with open(latest_txt_path, 'r') as f:
        content = f.read()
        assert content == snapshot_path
