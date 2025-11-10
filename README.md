# NotionSafe: Your Notion Workspace Backup Tool

NotionSafe is a cross-platform desktop application built with Python and PySide6 to create secure, local backups of your Notion workspaces. It provides a robust, versioned backup solution with both a graphical user interface (GUI) and a command-line interface (CLI).

![NotionSafe Logo](./assets/logo.png)

## Features

- **Cross-Platform GUI**: An easy-to-use graphical interface for configuration and backups, built with PySide6 to run on Windows, macOS, and Linux.
- **Configuration Wizard**: A simple, step-by-step wizard to get you started quickly.
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
If you have the GUI open, simply click the **"Run Backup Now"** button. You can view the progress in the log viewer window.

#### From the Command Line
To run a backup from the command line, execute the `cli` module:
```bash
python -m notebackup.cli
```

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
│   └── storage.py
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
