# NotionSafe: Your Notion Workspace Backup Tool

NotionSafe is a cross-platform desktop application built with Python and PySide6 to create secure, local backups of your Notion workspaces. It provides a robust, versioned backup solution with both a graphical user interface (GUI) and a command-line interface (CLI).

![NotionSafe Logo](./assets/logo.png)

## Features

- **Cross-Platform GUI**: An easy-to-use graphical interface for configuration and backups, built with PySide6 to run on Windows, macOS, and Linux.
- **Configuration Wizard**: A simple, step-by-step wizard to get you started quickly.
- **OS-level Scheduled Backups**: Easily set up and manage automatic backups using your operating system's native task scheduler directly from the GUI.
- **Robust Git Backups**: Automatically backs up your workspace to a Git repository with a unique two-branch strategy:
    - `history` branch: Contains a complete, versioned history of every snapshot.
    - `master` branch: Always reflects the content of the very latest backup.
- **Multiple Sync Targets**: Store your backups in a local folder, copy them to an external drive, and push them to a remote Git repository.
- **Secure Token Storage**: Your Notion API token is stored securely in your operating system's native keyring.
- **Comprehensive Test Suite**: A full suite of `pytest` tests ensures application stability and reliability.

## Installation and Usage

### 1. Prerequisites
- Python 3.10 or newer.

### 2. Installation
Clone the repository and install the required dependencies.

```bash
git clone https://github.com/Gfreak412/notionsafe.git
cd notionsafe

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

You can configure NotionSafe using the GUI (recommended) or by creating the configuration file manually.

#### GUI (Recommended)
Run the GUI application. It will detect that you have no configuration and automatically launch the setup wizard.

```bash
python -m notebackup.gui
```
The wizard will guide you through:
1.  Setting your Notion API token.
2.  Choosing a local directory for your backups.
3.  Optionally, configuring a Git repository for versioned backups.
4.  Optionally, configuring an external drive to copy backups to.

#### Manual Configuration
1. Create a configuration file at `~/.noteback/config.yaml` (on Linux/macOS) or `C:\Users\<YourUser>\.noteback\config.yaml` (on Windows).
2. Copy the contents of `examples/backup_config.yaml` into your new file and edit the values to match your setup.

### 4. Running a Backup

#### From the GUI
If you have the GUI open, simply click the **"Run Manual Backup"** button to perform a one-time backup. You can view the progress in the log viewer window.

For automatic backups, use the **"Install Scheduled Task"** and **"Uninstall Scheduled Task"** buttons. The backup frequency can be configured in your `~/.noteback/config.yaml` file under the `storage` section (e.g., `backup_frequency_hours: 24`).

#### From the Command Line
To run a backup from the command line, execute the `cli` module:
```bash
python -m notebackup.cli
```

## 5. Troubleshooting and FAQs

### Q: A CMD window still pops up when the scheduled task runs!
**A:** This is a common issue with Windows Task Scheduler. Even when using `pythonw.exe` or other silent launchers, the Task Scheduler might still force a console window to appear due to its default settings.

**Resolution:** You need to manually adjust a setting within the Task Scheduler GUI:
1.  **Open Task Scheduler:** Search for "Task Scheduler" in the Windows Start Menu.
2.  **Locate the Task:** Navigate to `Task Scheduler Library` and find `NotionSafeBackup`.
3.  **Access Task Properties:** Right-click on `NotionSafeBackup` and select `Properties`.
4.  **Check "General" Tab:**
    *   Under "Security options", ensure **"Run whether user is logged on or not"** is selected.
    *   If you change this, you will be prompted to enter the password for the user account under which the task will run. This is necessary for the task to run silently in the background.
    *   Also, ensure **"Run with highest privileges"** is checked.
5.  Click `OK` to save changes.

### Q: The scheduled task seems to be stuck in a loop or running too frequently.
**A:** This usually happens if the task is configured to restart on failure, and the backup script is encountering an error.

**Resolution:** Check the task's restart settings:
1.  **Open Task Scheduler** and locate `NotionSafeBackup` (as above).
2.  **Access Task Properties** and go to the `Settings` tab.
3.  **"If the task fails, restart every:"**:
    *   **Recommendation:** Uncheck this box if you don't want the task to restart automatically on failure.
    *   **Alternative:** If restarts are desired, set the interval to a very long period (e.g., `1 day`) and set "Attempt to restart up to:" to a low number (e.g., `1` or `2`).
4.  Click `OK` to save changes.

## Development

- **Linting**: `flake8 .` and `black .`
- **Testing**: `pytest`

## Project Structure

```
.
├── notebackup/
│   ├── __init__.py
│   ├── auth.py
│   ├── cli.py
│   ├── config_wizard.py
│   ├── exporter.py
│   ├── fs_layout.py
│   ├── gitops.py
│   ├── gui.py
│   ├── logger.py
│   ├── notion_api.py
│   ├── scheduler.py
│   ├── storage.py
│   └── task_scheduler.py
├── tests/
│   ├── test_auth.py
│   ├── test_cli.py
│   └── ... (and other tests)
├── assets/
│   └── logo.png
├── examples/
│   └── backup_config.yaml
├── .gitignore
├── pyproject.toml
└── requirements.txt
```
