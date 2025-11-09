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
| `config_wizard.py` | **Buggy** | GUI-based configuration wizard. Has missing widget init code. |
| `exporter.py` | **Implemented** | Core exporting logic is complete and tested. |
| `fs_layout.py`| **Implemented** | Handles snapshot directory creation. |
| `gitops.py` | **Implemented** | Fully integrated Git backup logic. |
| `gui.py` | **Buggy** | Main GUI application window. Has incorrect enum usage. |
| `logger.py` | **Implemented** | Centralized logging configuration. |
| `notion_api.py`| **Implemented** | Basic wrapper for the Notion API. |
| `scheduler.py`| **Implemented** | Cross-platform, in-process scheduler using the `schedule` library. |
| `storage.py` | **Implemented** | Handles external drive copy logic. |

## 4. Architectural Decisions

- **Test-Driven Development (TDD):** The project follows a strict TDD approach for new feature development, especially for the CLI. This ensures that the code is well-tested and that regressions can be caught early.
- **Cross-Platform Compatibility:** A key goal is to make the application cross-platform. This involves replacing platform-specific shell script calls with pure Python libraries.
- **Modularity:** The application is structured into modules with specific responsibilities, such as `auth`, `storage`, `exporter`, etc. This promotes code organization and reusability.

## 5. Session Log

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

### Session 7 (2025-11-07)

- **Goal:** Fix a `FileNotFoundError` that was occurring during the Git backup process.
- **Accomplishments:**
    - Diagnosed and fixed a series of complex, cascading bugs in the `gitops.py` module.
    - Resolved a `FileNotFoundError` caused by a stale bytecode cache and a subsequent logic error in file handling.
    - Systematically debugged a persistent Git authentication failure, transitioning from a problematic SSH setup to a robust HTTPS with Personal Access Token (PAT) method.
    - Diagnosed and fixed a `403 Forbidden` error by identifying incorrect PAT scopes (fine-grained vs. classic tokens).
    - Resolved a `PermissionError` on Windows by correctly managing `GitPython` object lifecycles to prevent file locking.
- **Outcome:** The Git backup feature is now fully robust and functional. The application is stable.

### Session 6 (2025-11-06)

- **Goal:** Fix critical bugs in the GUI and Configuration Wizard discovered during end-of-session testing.
- **Next Steps:**
    - **Fix `config_wizard.py`:** An `AttributeError` occurs because the widget creation code (e.g., `self.token_edit = QLineEdit()`) was omitted from the `__init__` methods of the wizard pages in the last refactoring. The plan is to add the widget and layout code back into the `__init__` methods.
    - **Fix `gui.py`:** A repeating `AttributeError` occurs in the `append_text` method because `cursor.End` is used instead of the correct enum `QTextCursor.MoveOperation.End`. The plan is to correct the attribute and add the necessary `from PySide6.QtGui import QTextCursor` import.

### Session 5 (2025-11-06)

- **Goal:** Resolve outstanding bugs from the previous session and implement major new features based on the user's direction.
- **Accomplishments:**
    - **Markdown Post-Processing:** Iteratively debugged and fixed the `post_process.py` script to correctly handle Notion's exported Markdown.
    - **Core Logic Fixes:** Modified storage logic and enabled image downloading by default.
    - **GitOps Refactoring:** Fully integrated the `gitops.py` module.
    - **GUI Implementation:** Created a functional GUI application with a live log viewer.
    - **GUI Configuration Wizard:** Created a comprehensive, multi-page configuration wizard to replace the CLI script.
    - **Centralized Logging:** Implemented a centralized logging system and refactored the application to use it.
- **Outcome:** The application is now significantly more robust and feature-rich, but contains critical bugs discovered in final testing.

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