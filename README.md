# NotionSafe: Your Notion Workspace Backup Tool

NotionSafe is a cross-platform desktop application built with Python to create secure, local backups of your Notion workspaces. It provides a robust, versioned backup solution with a native graphical user interface (GUI) for both Windows and Linux, as well as a full-featured command-line interface (CLI).

![NotionSafe Logo](./assets/logo.png)

## Features

- **Native Cross-Platform GUI**: An easy-to-use graphical interface for configuration and backups.
    - **Windows**: Built with PySide6 (Qt).
    - **Linux**: Built with PyGObject (GTK4) for a native desktop experience.
- **Configuration Wizard**: A simple, step-by-step wizard to get you started quickly on the first run.
- **OS-Native Scheduled Backups**: Easily set up and manage automatic backups using your operating system's native task scheduler (`schtasks` on Windows, `systemd` on Linux) directly from the GUI.
- **Robust Git Backups**: Automatically backs up your workspace to a Git repository with a unique two-branch strategy:
    - `history` branch: Contains a complete, versioned history of every snapshot.
    - `master` branch: Always reflects the content of the very latest backup.
- **Multiple Sync Targets**: Store your backups in a local folder, copy them to an external drive, and push them to a remote Git repository.
- **Secure Token Storage**: Your Notion API token is stored securely in your operating system's native keyring.
- **Comprehensive Test Suite**: A full suite of `pytest` tests ensures application stability and reliability.

## Installation and Usage

### 1. Prerequisites
- Python 3.10 or newer.
- For Linux, you will need GTK4 and related development libraries. See the [Linux Development Guide](#linux-development-guide-fedora) for details.

### 2. Installation
Clone the repository and install the application.

```bash
git clone https://github.com/Gfreak412/notionsafe.git
cd notionsafe

# Create and activate a virtual environment (recommended)
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/macOS
source venv/bin/activate

# Install dependencies for your OS
# On Windows
pip install -r requirements.txt
# On Linux
pip install -r requirements-linux.txt

# Install the application in editable mode
pip install -e .
```

### 3. Running NotionSafe

Once installed, you can run the application from your terminal using the `notionsafe` command.

```bash
notionsafe
```

The application will automatically detect your operating system and launch the appropriate GUI (Qt on Windows, GTK on Linux).

If it's your first time running the app, a configuration wizard will launch to guide you through:
1.  Setting your Notion API token.
2.  Choosing a local directory for your backups.
3.  Optionally, configuring a Git repository for versioned backups.
4.  Optionally, configuring an external drive to copy backups to.

### 4. Command-Line Interface (CLI)

To run a backup directly from the command line, use the `cli` command:
```bash
python -m notebackup.cli
```

## Project Structure

The project has been refactored to separate core logic from the UI and OS-specific components.

```
.
├── notebackup/
│   ├── __main__.py         # Main entry point, launches correct UI
│   ├── cli.py              # Command-line interface logic
│   ├── core.py             # Core backup worker logic (UI-agnostic)
│   ├── auth.py
│   ├── exporter.py
│   ├── fs_layout.py
│   ├── gitops.py
│   ├── logger.py
│   ├── notion_api.py
│   ├── storage.py
│   ├── os_scheduler/       # OS-native scheduling
│   │   ├── linux.py
│   │   └── windows.py
│   └── ui/                 # UI implementations
│       ├── qt_ui.py
│       ├── qt_config_wizard.py
│       ├── gtk_ui.py
│       └── gtk_config_wizard.py
├── tests/
│   └── ... (tests for all modules)
├── assets/
│   └── logo.png
├── .gitignore
├── pyproject.toml
├── requirements.txt        # Windows requirements
└── requirements-linux.txt  # Linux requirements
```

---
## Linux Development Guide (Fedora)

This guide provides a comprehensive, step-by-step process for setting up a development environment for NotionSafe on a bare-metal Fedora installation. A bare-metal or full VM environment is required to properly test native Linux features like `systemd` timers.

### Step 1: Update Your System
```bash
sudo dnf update
```

### Step 2: Install Build and GUI Dependencies
Install GCC, Python headers, and the necessary GTK4 and `libsecret` libraries.
```bash
sudo dnf install gcc python3-devel gtk4-devel gobject-introspection-devel cairo-gobject-devel libsecret-devel
```

### Step 3: Set Up Project
Clone the repository and set up your Python virtual environment.
```bash
git clone https://github.com/Gfreak412/notionsafe.git
cd notionsafe

python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
Install all the required Python libraries for Linux, then install the application in editable mode.
```bash
pip install -r requirements-linux.txt
pip install -e .
```

### Step 5: Run and Test
You can now run the GTK application and test its functionality, including the `systemd` scheduler integration.

#### Running the GUI
```bash
notionsafe
```
The GTK user interface should launch.

#### Testing the Systemd Scheduler
1.  Run the application (`notionsafe`) and complete the configuration wizard.
2.  Navigate to the **Scheduler** tab.
3.  Click the **Enable Scheduled Backup** button.
4.  Verify the timer's status:
    ```bash
    # Check the status of the timer
    systemctl --user status notionsafe-backup.timer

    # List all user timers to see when it's scheduled to run next
    systemctl --user list-timers
    ```

### Development FAQs

#### Q: Why can't I test `systemd` timers in WSL?
**A:** The Windows Subsystem for Linux (WSL) does not use a traditional `systemd` init process, which is required to manage `systemd` services and timers. Therefore, testing features that rely on native system services requires a full Linux installation (either bare-metal or in a VM).
