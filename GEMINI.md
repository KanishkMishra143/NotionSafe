
# GEMINI Project Context: NotionSafe

## Project Overview

This project, **NotionSafe**, is a Python-based application for creating secure, local backups of a Notion workspace. It is designed as a Linux-first, cross-platform desktop application with both a command-line interface (CLI) and a planned graphical user interface (GUI).

The core functionality involves fetching Notion pages and databases, exporting them to Markdown, and storing them in timestamped snapshot directories. It supports multiple backup targets, including a local folder, an external drive via `rsync`, and a remote Git repository using a specialized branching strategy.

**Key Technologies:**
- **Language:** Python 3.10+
- **GUI:** PySide6 (stubbed)
- **Notion API:** `notion-client` and `notion2md`
- **Dependencies:** `PyYAML` for configuration, `keyring` for secure token storage, `GitPython` for git operations.
- **System Tools:** `git`, `git-lfs`, `rsync`.

**Architecture:**
- The main application logic is encapsulated in the `notebackup` Python package.
- The entry point for the backup process is `scripts/backup_runner.py`, which uses the `notebackup.cli` module.
- Configuration is managed via a YAML file located at `~/.noteback/config.yaml`.
- Automation is handled by shell scripts for git operations (`git_commit_update.sh`), `rsync` (`rsync_copy.sh`), and scheduling (`install_systemd_timer.sh`).

## Building and Running

The project uses a shell script (`setup.sh`) for easy installation on Linux systems.

**1. Installation:**
To install system dependencies (e.g., `git`, `python3`, `rsync`) and Python packages into a virtual environment, run:
```bash
bash setup.sh --install
```

**2. Running the Backup:**
After installation, activate the virtual environment and run the main backup script:
```bash
source venv/bin/activate
python scripts/backup_runner.py
```
- **Configuration:** Before the first run, copy `examples/backup_config.yaml` to `~/.noteback/config.yaml` and populate it with your Notion Page/Database IDs and storage preferences.
- **Authentication:** Set the `NOTION_TOKEN` environment variable or run the script once to be prompted to save the token to the system's keyring.

**3. Testing and Linting:**
The project is set up with `pytest` for testing and `black` and `flake8` for code quality.
- **Testing:**
  ```bash
  pytest
  ```
- **Linting:**
  ```bash
  flake8 .
  black .
  ```

## Development Conventions

- **Branching Model:** The Git repository uses a unique branching strategy:
    - `backup` branch: Contains a complete history of all timestamped snapshot folders.
    - `main` branch: Contains only the contents of the *latest* snapshot. This branch is force-pushed on each backup run.
- **Git LFS:** Attachments and other binary files (e.g., `.pdf`, `.png`, `.mp4`) are tracked using Git LFS to keep the main repository lightweight. The configuration is in `.gitattributes`.
- **Configuration:** All settings are externalized to the `~/.noteback/config.yaml` file, including Notion page IDs, storage paths, and sync target settings.
- **Security:** Notion API tokens are not stored in plaintext. The application retrieves the token from the `NOTION_TOKEN` environment variable or, preferably, from the secure OS keyring via the `keyring` library.
- **Scheduling:** The project supports `systemd` timers and `cron` jobs for automated backups on Linux. The `scripts/install_systemd_timer.sh` script provides an easy setup for `systemd`.
