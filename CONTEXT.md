# CONTEXT.md: NotionSafe Project

This document provides a detailed context for the NotionSafe project for the Gemini assistant, ensuring consistency and a shared understanding across multiple development sessions.

## 1. Project Overview

**NotionSafe** is a Python-based application for creating secure, local backups of a Notion workspace. The primary goal is to provide a reliable and easy-to-use tool for users to back up their valuable Notion data.

The project is being developed with a focus on a robust command-line interface (CLI) for Windows 11, with a future goal of creating a cross-platform graphical user interface (GUI) for both Windows and Linux.

**Repository:** https://github.com/KanishkMishra143/NotionSafe

## 2. Key Technologies

- **Language:** Python 3.10+
- **GUI:** PySide6
- **Testing:**
    - `pytest` for test automation.
    - `pytest-mock` for mocking objects and functions in tests.
- **Dependencies:**
    - `PyYAML` for reading and parsing the configuration file.
    - `keyring` for securely storing the Notion API token.
    - `GitPython` for interacting with git repositories for versioned backups.

## 3. Module Implementation Status

| Module | Status | Notes |
| :--- | :--- | :--- |
| `auth.py` | **Implemented** | Handles Notion token retrieval. |
| `cli.py` | **Implemented** | Core backup logic. Refactored to use `logging`. |
| `config_wizard.py` | **Implemented** | GUI wizard is now functional. |
| `exporter.py` | **Implemented** | Core exporting logic is complete and tested. |
| `fs_layout.py`| **Implemented** | Handles snapshot directory creation. |
| `gitops.py` | **Implemented and hardened** | Fully integrated and robust Git backup logic. |
| `gui.py` | **Implemented** | Main GUI application is now functional. |
| `logger.py` | **Implemented** | Centralized logging configuration. |
| `notion_api.py`| **Implemented** | Basic wrapper for the Notion API. |
| `scheduler.py`| **Implemented** | Cross-platform, in-process scheduler using the `schedule` library. |
| `storage.py` | **Implemented** | Handles external drive copy logic. |

## 4. Architectural Decisions

- **Test-Driven Development (TDD):** The project follows a strict TDD approach for new feature development, especially for the CLI. This ensures that the code is well-tested and that regressions can be caught early.
- **Cross-Platform Compatibility:** A key goal is to make the application cross-platform. This involves replacing platform-specific shell script calls with pure Python libraries.
- **Modularity:** The application is structured into modules with specific responsibilities, such as `auth`, `storage`, `exporter`, etc. This promotes code organization and reusability.

## 5. Session Log

### Session 10 (2025-11-10)

- **Goal:** Fix a bug where the Git `history` branch would not update if the backup directory was changed.
- **Accomplishments:**
    - Diagnosed the root cause in `notebackup/gitops.py`: the code was initializing a new repository instead of cloning the existing one.
    - Implemented a robust fix: the code now clones the remote into a temporary directory and moves the `.git` folder into the new backup path, correctly preserving history.
    - The fix also handles cases where the remote repository is empty, gracefully falling back to creating a new one.
    - Updated the test suite (`tests/test_gitops.py`) to reflect the new, more complex logic, ensuring the fix was validated and didn't cause regressions.
    - Ran the full test suite successfully, confirming the project's stability.
- **Outcome:** The critical bug is resolved, and the `gitops` module is significantly more resilient. The project is stable and ready for further development.

### Session 9 (2025-11-09)

- **Goal:** Fix a git authentication bug and improve the project's test coverage.
- **Accomplishments:**
    - Fixed a `credential url cannot be parsed` error in `notebackup/gitops.py` by removing a problematic `custom_environment` block.
    - Repaired the entire test suite, which was failing due to outdated and brittle tests.
    - Refactored `notebackup/cli.py` to separate config loading from the main backup logic, improving testability.
    - Created a comprehensive test suite with 20 tests covering all core, non-GUI modules (`gitops.py`, `fs_layout.py`, `notion_api.py`, `logger.py`, `auth.py`, and `scheduler.py`).
    - Investigated and explained a markdown formatting issue and a user-reported issue with a git URL.
- **Outcome:** The project is now in a very stable state with a solid test suite, ready for new feature development.

### Session 8 (2025-11-07)

- **Goal:** Confirm that all bugs in the `gitops.py` module are resolved.
- **Accomplishments:**
    - Successfully ran a full backup without any errors, confirming the fixes from the previous session.
- **Outcome:** The application is confirmed to be stable and fully functional.

---

*Older sessions omitted for brevity.*

## 6. Future Directions

With the core functionality and a V1 GUI in place, future work can focus on polish, packaging, and deeper integration.

**Option 1: GUI Polish and Scheduler Integration**
   - **Goal**: Enhance the user experience of the GUI. This includes adding icons and progress bars, and more importantly, integrating the background scheduler. The GUI could have controls to start/stop the automated backup service and display the next scheduled run time.

**Option 2: Packaging and Distribution**
   - **Goal**: Make the application accessible to non-technical users by packaging it as a standalone executable. Using a tool like `PyInstaller` or `cx_Freeze`, we can create a `.exe` file for Windows that includes the Python interpreter and all dependencies, allowing users to run NotionSafe without installing Python or any packages.

**Option 3: Advanced Error Handling & Recovery**
   - **Goal**: Make the GUI smarter about errors. For example, if a backup fails due to an invalid Notion token, the GUI could detect this specific error and pop up a dialog that directly prompts the user to re-run the configuration wizard to fix it.
