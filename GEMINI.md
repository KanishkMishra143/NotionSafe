# GEMINI Project Context: NotionSafe

## Project Overview

This project, **NotionSafe**, is a Python-based application for creating secure, local backups of a Notion workspace. The immediate focus is on creating a robust command-line interface (CLI) on **Windows 11**, with a cross-platform graphical user interface (GUI) planned for both Windows and Linux. The project's repository is available at https://github.com/KanishkMishra143/NotionSafe.

The core functionality involves fetching Notion pages and databases, exporting them to Markdown, and storing them in timestamped snapshot directories. It supports multiple backup targets, including a local folder, an external drive, and a remote Git repository.

**Key Technologies:**
- **Language:** Python 3.10+
- **CLI TUI:** `rich`, `questionary`
- **GUI:** PySide6 (stubbed)
- **Notion API:** `notion-client` and `notion2md`
- **Dependencies:** `PyYAML` for configuration, `keyring` for secure token storage, `GitPython` for git operations.
- **System Tools:** `git`, `git-lfs`, `rsync` (for Linux/macOS).

**Architecture:**
- The main application logic is encapsulated in the `notebackup` Python package.
- The entry point for the backup process is `scripts/backup_runner.py`, which uses the `notebackup.cli` module.
- Configuration is managed via a YAML file located at `~/.noteback/config.yaml`.

---

## Current Status and Next Steps

### Current Status (as of end-of-session)
- **Interactive Configuration:** The `scripts/configure.py` script is functionally complete. It uses the `questionary` library to provide a user-friendly checklist for selecting pages and databases, and it successfully generates the `~/.noteback/config.yaml` file.
- **Testing Framework:** A `tests/` directory has been established for `pytest`. Test files for `notebackup/fs_layout.py` and `notebackup/exporter.py` have been created, and a strategy for mocking external dependencies is in place.
- **Development Environment:** The primary development environment has shifted from Linux to **Windows 11**.

### Next Steps
1.  **Implement Core Backup Logic:**
    - The main priority is to make `scripts/backup_runner.py` fully functional.
    - This involves enhancing `notebackup/cli.py` to:
        - Read the `~/.noteback/config.yaml` file.
        - Call the `notebackup.exporter` to convert Notion pages/databases to Markdown.
        - Use the `notebackup.storage` and `notebackup.gitops` modules to save the exported files to the user's chosen locations (local, external, Git).
2.  **Continue Test-Driven Development (TDD):**
    - As the core logic is implemented, continue to write and expand the `pytest` tests.
    - The immediate testing goal is to complete the tests for `notebackup/exporter.py` to ensure it handles various Notion content correctly.
3.  **Focus on Windows CLI:**
    - Ensure all CLI functionality is developed and tested primarily on Windows. Linux-specific scripts (e.g., `install_systemd_timer.sh`, `rsync_copy.sh`) are a lower priority.
4.  **GUI Development (Future):**
    - Once the CLI is stable and feature-complete, development on the cross-platform PySide6 GUI can begin.

---

## Testing and Code Quality
The project is set up with `pytest` for testing and `black` and `flake8` for code quality.

- **Linting:**
  ```bash
  flake8 .
  black .
  ```

- **Testing Strategy:**
  - **Directory Structure:** All tests are in the `tests/` directory, mirroring the `notebackup/` package structure. Test files `tests/test_fs_layout.py` and `tests/test_exporter.py` have been created.
  - **Tooling:** We use `pytest` and `pytest-mock` for mocking external dependencies.
  - **Execution:**
    ```bash
    pytest
    ```

## Development Conventions
- **Branching Model:** The Git repository uses a unique branching strategy:
    - `backup` branch: Contains a complete history of all timestamped snapshot folders.
    - `main` branch: Contains only the contents of the *latest* snapshot. This branch is force-pushed on each backup run.
- **Security:** Notion API tokens are stored securely in the OS keyring via the `keyring` library.