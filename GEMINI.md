# GEMINI Project Context: NotionSafe

## Project Overview

This project, **NotionSafe**, is a Python-based application for creating secure, local backups of a Notion workspace. The immediate focus is on creating a robust command-line interface (CLI) on **Windows 11**, with a cross-platform graphical user interface (GUI) planned for both Windows and Linux. The project's repository is available at https://github.com/KanishkMishra143/NotionSafe.

**Key Technologies:**
- **Language:** Python 3.10+
- **CLI TDD:** `pytest`, `pytest-mock`
- **Dependencies:** `PyYAML` for configuration, `keyring` for secure token storage, `GitPython` for git operations, `schedule` for in-process scheduling.

---

## Current Status and Next Steps

### Current Status (as of 2025-11-05)

- **User Interaction Rule**: Per the user's request, all interventions that write or modify code **must** be preceded by a question asking for explicit permission to do so.
- **Scheduler Refactored**: `notebackup/scheduler.py` has been successfully refactored to be a cross-platform, automated scheduler using the `schedule` library. The backup frequency is now configurable via `scripts/configure.py`.
- **Improved User Setup**: Created `setup.bat` and `run.bat` scripts to significantly improve the setup experience for new users on Windows.
- **Bug Fixes from User Testing**:
    - Fixed an error where the wrong argument (`--output` instead of `--path`) was being passed to the `notion2md` exporter.
    - Fixed a permissions error on Windows (`OSError: [WinError 1314]`) by replacing `os.symlink` with a `latest.txt` marker file for tracking the most recent backup.

### Module Implementation Status

| Module | Status | Notes |
| :--- | :--- | :--- |
| `auth.py` | **Implemented** | Handles Notion token retrieval. |
| `cli.py` | **Implemented** | Core backup logic is implemented and tested. |
| `exporter.py` | **Implemented** | Core exporting logic is complete and tested. |
| `fs_layout.py`| **Implemented** | Handles snapshot directory creation and `latest.txt` marker. |
| `gitops.py` | **Partially Implemented** | Contains `git` helper functions. Not fully integrated. |
| `gui_stub.py` | **Stub** | Placeholder for a future GUI. |
| `notion_api.py`| **Implemented** | Basic wrapper for the Notion API. |
| `scheduler.py`| **Implemented** | Cross-platform, in-process scheduler using the `schedule` library. |
| `storage.py` | **Implemented** | Refactored for cross-platform compatibility and tested. |

### Next Steps (for next session)

With the core CLI functionality now more robust and cross-platform, we can choose from several strategic directions for the next session:

**Option 1: Complete Git Operations (`gitops.py`)**
   - **Goal**: Fully integrate `gitops.py` to make the Git backup feature more robust and intelligent. This involves moving the Git logic from `storage.py` into `gitops.py` and enhancing it (e.g., auto-initialization, better error handling).

**Option 2: Begin GUI Development**
   - **Goal**: Start building the cross-platform graphical user interface (GUI) using `PySide6`, replacing the current `gui_stub.py`.

**Option 3: Enhance Application Robustness**
   - **Goal**: Improve the overall stability and user experience of the CLI application by implementing a centralized logging system (using Python's `logging` module) to provide better debugging and progress tracking than the current `print` statements.

---

## Testing and Code Quality

- **Linting:** `flake8 .`, `black .`
- **Execution:** `pytest`
