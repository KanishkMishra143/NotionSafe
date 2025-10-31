# NotionSafe

NotionSafe is a cross-platform desktop application to backup your Notion workspaces locally. It provides a robust solution for creating versioned snapshots of your Notion pages, including attachments, and storing them on your local machine, an external drive, or a Git repository.

## Features

- **Local First**: Your data is always stored on your machine.
- **Timestamped Snapshots**: Backups are organized in timestamped folders.
- **Multiple Sync Targets**:
  - Local folder
  - External HDD (via `rsync`)
  - Git repository (with `backup` and `main` branches)
- **Git LFS**: Attachments are handled efficiently using Git LFS.
- **Secure**: Notion tokens are stored securely in the OS keyring.
- **Schedulable**: Supports `cron` and `systemd` for automated backups.
- **Cross-Platform**: Built with Python and Qt (PySide6), with plans for AppImage (Linux) and PyInstaller (Windows) packaging.

## Quick Start

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/notionsafe.git
    cd notionsafe
    ```

2.  **Run the installer:**
    This script will detect your Linux distribution, install system dependencies, create a Python virtual environment, and install the required packages.
    ```bash
    bash setup.sh --install
    ```

3.  **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```

4.  **Configure Notion Integration:**
    - Create a Notion integration: [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
    - Share the pages/databases you want to backup with your integration.
    - Set your Notion API token as an environment variable:
      ```bash
      export NOTION_TOKEN="your_secret_token"
      ```
      Alternatively, the application will prompt you to save the token securely in your OS keyring on the first run.

5.  **Configure your backup:**
    Copy the example configuration file and edit it to your needs.
    ```bash
    mkdir -p ~/.noteback
    cp examples/backup_config.yaml ~/.noteback/config.yaml
    # Edit ~/.noteback/config.yaml
    ```

6.  **Run your first backup:**
    ```bash
    python scripts/backup_runner.py
    ```

## Commands

The `setup.sh` script creates several helper scripts in the `scripts/` directory:

-   `backup_runner.py`: The main script to perform a backup.
-   `git_commit_update.sh`: Commits snapshots to the `backup` branch and updates the `main` branch.
-   `rsync_copy.sh`: Copies the latest snapshot to an external drive.
-   `install_systemd_timer.sh`: Installs a systemd user timer for automated backups.

## Development

-   **Linting**: `flake8 .` and `black .`
-   **Testing**: `pytest`

## Project Structure

```
.
├── examples/
│   └── backup_config.yaml
├── notebackup/
│   ├── auth.py
│   ├── cli.py
│   ├── exporter.py
│   ├── fs_layout.py
│   ├── gitops.py
│   ├── gui_stub.py
│   ├── notion_api.py
│   ├── scheduler.py
│   └── storage.py
├── scripts/
│   ├── backup_runner.py
│   ├── git_commit_update.sh
│   ├── install_systemd_timer.sh
│   └── rsync_copy.sh
├── .gitattributes
├── .gitignore
├── pyproject.toml
├── README.md
├── requirements.txt
└── setup.sh
```
