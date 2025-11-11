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

# GEMINI Project Context: NotionSafe

## Project Overview

This project, **NotionSafe**, is a Python-based application for creating secure, local backups of a Notion workspace. It features a command-line interface (CLI) and a graphical user interface (GUI) built with PySide6.

**Key Technologies:**
- **Language:** Python 3.10+
- **GUI:** PySide6
- **Dependencies:** `PyYAML`, `keyring`, `GitPython`, `schedule`, `notion-client`

---

## Current Status (as of 2025-11-11)

- **Cross-Platform Scheduled Task Management:** Implemented robust, OS-native scheduled task management for both Windows (schtasks) and Linux (systemd), ensuring silent and reliable automatic backups across platforms.
- **Advanced Error Handling for Invalid Notion Token:** The GUI now intelligently detects invalid Notion API tokens during backup attempts and prompts the user to re-run the configuration wizard for correction.
- **Silent Scheduled Tasks:** Successfully implemented and configured scheduled tasks to run completely silently without spawning a CMD window, resolving a persistent UI issue.
- **Robust Error Handling:** Implemented robust error handling for the core backup process, preventing silent failures from the underlying exporter and ensuring graceful degradation.
- **GitOps Hardened:** Systematically debugged and fixed a series of cascading bugs in the `gitops.py` module, resulting in a fully robust and functional Git backup feature.
- **Comprehensive Test Suite:** Created and repaired a comprehensive test suite with 20 tests covering all core modules. This significantly improves project stability and maintainability.
- **Backup End-to-End Success:** A full backup process, including Git remote push, completed successfully, confirming all recent bug fixes.
- **Critical Bugs Fixed:** The `AttributeError` crashes in the Configuration Wizard and GUI Log Viewer have been resolved.
- **Markdown Post-Processing:** A robust script (`post_process.py`) is in place to fix `notion2md` output.
- **GUI Implemented:** The application has a functional GUI.
- **GUI Configuration Wizard:** The configuration wizard is implemented and functional.
- **Centralized Logging:** A centralized logging system is fully implemented and integrated.

### Module Implementation Status

| Module | Status | Notes |
| :--- | :--- | :--- |
| `auth.py` | **Implemented** | Handles Notion token retrieval. |
| `cli.py` | **Implemented** | Core backup logic. Now with robust error checking on exporter and `InvalidNotionTokenError` handling. |
| `config_wizard.py` | **Implemented** | GUI wizard is now functional. |
| `exporter.py` | **Implemented** | Core exporting logic. Now with enhanced error logging. |
| `fs_layout.py`| **Implemented** | Handles snapshot directory creation and `latest.txt` marker. |
| `gitops.py` | **Implemented and hardened** | Fully integrated and robust Git backup logic. |
| `gui.py` | **Implemented** | Main GUI application is now functional, with `InvalidNotionTokenError` handling. |
| `logger.py` | **Implemented** | Centralized logging configuration improved for background tasks. |
| `notion_api.py`| **Implemented** | Basic wrapper for the Notion API. |
| `scheduler.py`| **Implemented** | Cross-platform, in-process scheduler. Not yet integrated with GUI. |
| `storage.py` | **Implemented** | Handles external drive copy logic. |
| `task_scheduler.py`| **Implemented** | Manages OS-native scheduled tasks, now with silent execution and Linux systemd support. |

---

## Session Log

### Session 15 (2025-11-11)
- **Goal:** Implement cross-platform scheduled task management for Linux using `systemd` timers.
- **Accomplishments:**
    - Modified `notebackup/task_scheduler.py` to include `platform` detection.
    - Implemented `create_task_linux_systemd` to generate and install `.service` and `.timer` files for `systemd`. This includes setting `ExecStart` to the Python executable and `backup_runner.py`, `WorkingDirectory` to the project root, and `OnUnitActiveSec` based on the configured interval.
    - Implemented `delete_task_linux_systemd` to stop, disable, and remove the `systemd` service and timer files.
    - Updated the main `create_task` and `delete_task` functions to dispatch to the appropriate OS-specific implementation (Windows `schtasks` or Linux `systemd`).
- **Outcome:** NotionSafe now supports robust, OS-native scheduled backups on both Windows and Linux, enhancing its cross-platform capabilities.

### Session 14 (2025-11-11)
- **Goal:** Implement advanced error handling in the GUI for invalid Notion API tokens.
- **Accomplishments:**
    - Defined a custom exception `InvalidNotionTokenError` in `notebackup/cli.py`.
    - Modified `notebackup/cli.py` to raise `InvalidNotionTokenError` when `notion_client.Client` initialization or a test API call fails due to an unauthorized (401) error.
    - Modified `notebackup/gui.py`:
        - Added a new signal `invalid_token_error` to the `Worker` class.
        - Updated the `Worker.run()` method to catch `InvalidNotionTokenError` and emit the new signal.
        - Connected the `worker.invalid_token_error` signal to a new `handle_invalid_token_error` slot in `MainWindow`.
        - Implemented `handle_invalid_token_error` to display a `QMessageBox` informing the user about the invalid token and prompting them to re-run the configuration wizard.
        - Ensured that scheduled jobs also log the `InvalidNotionTokenError` appropriately.
- **Outcome:** The GUI now provides clear, actionable feedback to the user when their Notion API token is invalid, guiding them to resolve the issue by re-running the configuration wizard.

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

With the core functionality stabilized, future work can focus on packaging and usability enhancements.

**Option 1: Packaging and Distribution**
   - **Goal**: Make the application accessible to non-technical users by packaging it as a standalone executable using a tool like `PyInstaller` or `cx_Freeze`.

**Option 2: GUI Scheduler Integration**
   - **Goal**: Integrate the background scheduler with the GUI. This will involve creating a dedicated "Scheduler" tab, adding controls (e.g., buttons, status indicators) to manage the scheduled backup service, and displaying its status (e.g., "Running", "Stopped", "Next backup at...").
   - **Implementation**: This will likely involve creating a new module to manage interaction with the OS-native task scheduler (Windows Task Scheduler and `systemd` on Linux) to ensure reliability.