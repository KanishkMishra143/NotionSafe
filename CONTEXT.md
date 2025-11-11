<!--=====================================================================================-->
# Instructions for GEMINI

This section outlines the preferred workflow and instructions for the Gemini assistant to ensure efficient and aligned collaboration.

-   **No Automatic Git Operations**: Do not automatically stage (`git add .`) or commit changes unless explicitly instructed to do so. Wait for explicit instructions regarding Git operations.
-   **Provide Testing Instructions**: Instead of running tests or verifying changes yourself, provide clear, step-by-step instructions for the user to perform testing and verification.
-   **Avoid Unsolicited Command Execution**: Do not execute any shell commands that modify the system or codebase without explicit instruction and confirmation from the user. Always propose the command and await approval.
<!--
DO NOT REMOVE THIS COMMENT. This instructions is central to the design and
safety of the NotionSafe backup process. Future modifications must adhere
to these instructions.
=====================================================================================
-->
---

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
| `cli.py` | **Implemented** | Core backup logic. Now with robust error checking on exporter. |
| `config_wizard.py` | **Implemented** | GUI wizard is now functional. |
| `exporter.py` | **Implemented** | Core exporting logic. Now with enhanced error logging. |
| `fs_layout.py`| **Implemented** | Handles snapshot directory creation and `latest.txt` marker. |
| `gitops.py` | **Implemented and hardened** | Fully integrated and robust Git backup logic. |
| `gui.py` | **Implemented** | Main GUI application is now functional. |
| `logger.py` | **Implemented** | Centralized logging configuration improved for background tasks. |
| `notion_api.py`| **Implemented** | Basic wrapper for the Notion API. |
| `scheduler.py`| **Implemented** | Cross-platform, in-process scheduler. Not yet integrated with GUI. |
| `storage.py` | **Implemented** | Handles external drive copy logic. |
| `task_scheduler.py`| **Implemented** | Manages OS-native scheduled tasks, now with silent execution. |

## 4. Architectural Decisions

- **Test-Driven Development (TDD):** The project follows a strict TDD approach for new feature development, especially for the CLI. This ensures that the code is well-tested and that regressions can be caught early.
- **Cross-Platform Compatibility:** A key goal is to make the application cross-platform. This involves replacing platform-specific shell script calls with pure Python libraries.
- **Modularity:** The application is structured into modules with specific responsibilities, such as `auth`, `storage`, `exporter`, etc. This promotes code organization and reusability.

## 5. Session Log

### Session 13 (2025-11-11)
- **Goal:** Resolve the persistent issue of a CMD window popping up when the scheduled backup task runs.
- **Accomplishments:**
    - Investigated and attempted multiple standard methods for suppressing console windows:
        - Using `cmd.exe /c start /b` with the batch file.
        - Direct execution of `pythonw.exe`.
        - VBScript wrapper (`run_hidden.vbs`) using `WshShell.Run` with `windowStyle = 0`.
        - PowerShell wrapper (`run_silent.ps1`) using `Start-Process -WindowStyle Hidden`.
        - Python launcher (`launch_hidden.py`) using `subprocess.Popen` with `STARTUPINFO` and `SW_HIDE`.
    - Diagnosed that the issue was not with the Python code or scripting wrappers, but with a specific default setting in the Windows Task Scheduler GUI.
    - Modified `notebackup/task_scheduler.py` to automatically set the task to "Run whether user is logged on or not" and "Run with highest privileges" (`/ru SYSTEM`, `/rl HIGHEST`) during task creation.
    - Provided step-by-step instructions to the user to manually change the "Security options" in the Task Scheduler's "General" tab to "Run whether user is logged on or not" for existing tasks.
    - Confirmed with the user that this manual change successfully resolved the CMD window popping up.
- **Outcome:** The scheduled backup task now runs completely silently without any CMD window appearing. The application's task scheduling is robust and user-friendly.

### Session 12 (2025-11-11)
- **Goal:** Debug and fix a scheduled task failure where backups were failing intermittently, creating and pushing empty directories to the git remote.
- **Accomplishments:**
    - Diagnosed that the backup process was not checking the return code from the `notion2md` exporter, causing it to fail silently.
    - Modified `notebackup/cli.py` to check the exporter's return code and raise an exception on failure, ensuring the backup process stops correctly.
    - Improved the logging configuration by modifying `notebackup/logger.py` to allow logs to propagate, enabling centralized logging and easier debugging of background tasks.
    - Enhanced `notebackup/exporter.py` to capture `stdout` and `stderr` from the exporter subprocess, ensuring detailed error messages are available for future debugging.
    - Confirmed that the fix correctly handles intermittent exporter failures, preventing empty directories from being pushed and providing clear error logs.
- **Outcome:** The application is now robust against intermittent export failures from the underlying `notion2md` library. The backup process fails gracefully and provides detailed logs, improving reliability and maintainability.

### Session 11 (2025-11-10)
- **Goal:** Fix the final bugs in the `gitops.py` module and ensure the test suite is passing.
- **Accomplishments:**
    - Diagnosed a complex bug where creating the snapshot inside the git repository working directory caused `git pull` to fail due to "unstaged changes".
    - Refactored `gitops.py` to temporarily move the new snapshot out of the working directory before performing git operations, ensuring a clean state.
    - Iteratively debugged and fixed the corresponding unit test in `tests/test_gitops.py`.
    - Successfully ran the entire 20-test suite, confirming the stability of the application.
- **Outcome:** The `gitops` feature is now fully functional and robustly tested. The project is stable and the core features are complete.

### Session 10 (2025-11-10)
- **Goal:** Fix a bug where the Git `history` branch would not update if the backup directory was changed.
- **Accomplishments:**
    - Diagnosed the root cause in `notebackup/gitops.py`: the code was initializing a new repository instead of cloning the existing one.
    - Implemented a robust fix: the code now clones the remote into a temporary directory and moves the `.git` folder into the new backup path, correctly preserving history.
    - Updated the test suite (`tests/test_gitops.py`) to reflect the new, more complex logic.
- **Outcome:** The critical bug is resolved, and the `gitops` module is significantly more resilient.

## 6. Future Directions

With the core functionality stabilized, future work can focus on GUI integration, packaging, and usability enhancements.

**Option 1: GUI Scheduler Integration**
   - **Goal**: Integrate the background scheduler with the GUI. This will involve creating a dedicated "Scheduler" tab, adding controls (e.g., buttons, status indicators) to manage the scheduled backup service, and displaying its status (e.g., "Running", "Stopped", "Next backup at...").
   - **Implementation**: This will likely involve creating a new module to manage interaction with the OS-native task scheduler (Windows Task Scheduler and `systemd` on Linux) to ensure reliability.

**Option 2: Packaging and Distribution**
   - **Goal**: Make the application accessible to non-technical users by packaging it as a standalone executable using a tool like `PyInstaller` or `cx_Freeze`.

**Option 3: Advanced Error Handling & Recovery**
   - **Goal**: Make the GUI smarter about errors. For example, if a backup fails due to an invalid Notion token, the GUI could detect this and prompt the user to re-run the configuration wizard.