# CONTEXT.md: NotionSafe Project

This document provides a detailed context for the NotionSafe project for the Gemini assistant, ensuring consistency and a shared understanding across multiple development sessions.

## 1. Project Overview

**NotionSafe** is a Python-based application for creating secure, local backups of a Notion workspace. The primary goal is to provide a reliable and easy-to-use tool for users to back up their valuable Notion data.

The project is being developed with a focus on a robust command-line interface (CLI) for Windows 11, with a future goal of creating a cross-platform graphical user interface (GUI) for both Windows and Linux.

**Repository:** https://github.com/KanishkMishra143/NotionSafe

## 2. Key Technologies

- **Language:** Python 3.10+
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
| `cli.py` | **Implemented** | Core backup logic is implemented and tested. |
| `exporter.py` | **Implemented** | Core exporting logic is complete and tested. |
| `fs_layout.py`| **Implemented** | Handles snapshot directory creation. |
| `gitops.py` | **Partially Implemented** | Contains `git` helper functions. |
| `gui_stub.py` | **Stub** | Placeholder for a future GUI. |
| `notion_api.py`| **Implemented** | Basic wrapper for the Notion API. |
| `scheduler.py`| **Implemented** | Cross-platform, in-process scheduler using the `schedule` library. |
| `storage.py` | **Implemented** | Refactored for cross-platform compatibility and tested. |

## 4. Architectural Decisions

- **Test-Driven Development (TDD):** The project follows a strict TDD approach for new feature development, especially for the CLI. This ensures that the code is well-tested and that regressions can be caught early.
- **Cross-Platform Compatibility:** A key goal is to make the application cross-platform. This involves replacing platform-specific shell script calls with pure Python libraries.
- **Modularity:** The application is structured into modules with specific responsibilities, such as `auth`, `storage`, `exporter`, etc. This promotes code organization and reusability.

## 5. Session Log

### Session 4 (2025-11-05)

- **Goal:** Fix the callout block conversion and address other user requests.
- **Accomplishments:**
    - Investigated the `notion2md` library to understand how it handles callout blocks.
    - Patched the `notion2md` library to handle external icons in callout blocks.
    - Created a post-processing script to convert callout blocks to the Obsidian-compatible syntax.
- **Next Steps:**
    - **Fix the post-processing script:** The `post_process.py` script is not working as expected and needs to be fixed.
    - **Address the user's new requests:**
        - Ensure that not only the contents of the snapshot directory are copied to the external drive, but the whole of the timestamped folder itself.
        - Ensure that all images and files are downloaded by default.
        - Explain the purpose of the `latest.txt` file.

### Session 3 (2025-11-05)

- **Goal:** Address the issues with the backup output format and content.
- **Accomplishments:**
    - Added error handling to the backup process to prevent it from failing when encountering problematic blocks.
- **Next Steps:**
    - **Investigate `notion2md` further:** Dive deeper into the `notion2md` library to see if it has any options to control the output format and file naming. Also, look for any information about Obsidian compatibility.
    - **POC for unzipping and renaming:** Create a small proof-of-concept to unzip the files and rename them using the page title. This will involve using the Notion API to get the page titles.
    - **Address Obsidian compatibility:** Identify the Notion-specific features that are not compatible with Obsidian and find a way to convert them. This might involve writing a custom script to post-process the Markdown files.

### Session 2 (2025-11-05)

- **Goal**: Make the scheduler cross-platform and improve the new user experience.
- **Accomplishments**:
    - Refactored `notebackup/scheduler.py` to use the `schedule` library, creating a cross-platform, in-process automated scheduler.
    - Modified `scripts/configure.py` to allow users to select a backup frequency ("Daily", "Weekly", "Monthly") and store it in the config.
    - Updated `scripts/backup_runner.py` to use the configured frequency.
    - Created `setup.bat` and `run.bat` to automate the environment setup and activation for Windows users, significantly improving the new user experience.
    - **Bug Fixes (from user testing):**
        - Corrected the `notion2md` call in `notebackup/cli.py` to use the `--path` argument instead of `--output`.
        - Replaced the permission-sensitive `os.symlink` in `notebackup/fs_layout.py` with a `latest.txt` marker file to prevent errors on Windows.
- **Outcome**: The application is now more robust, cross-platform, and significantly easier for a new Windows user to set up and run. Key bugs discovered during testing were resolved.

### Session 1 (2025-11-04)

- **Goal:** Refactor `tests/test_cli.py` and `notebackup/storage.py`.
- **Accomplishments:**
    - Refactored `tests/test_cli.py` to use a `mock_cli_env` fixture, reducing code duplication.
    - Refactored `notebackup/storage.py` for cross-platform compatibility:
        - Replaced `rsync` with `shutil` in `rsync_to_external`.
        - Replaced a `bash` script with `GitPython` in `git_commit`.
    - Added unit tests for the refactored functions in `tests/test_storage.py`.
- **Outcome:** All tests are passing. The `storage.py` module is now cross-platform.
