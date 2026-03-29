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
git clone https://github.com/KanishkMishra143/NotionSafe.git
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
# If you are testing on WSL
GSK_RENDERER=cairo notionsafe

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

```text
.
├── notebackup/                     # Application package
│   ├── __main__.py                 # OS-aware GUI launcher entrypoint
│   ├── core.py                     # UI-agnostic backup runner
│   ├── cli.py                      # Backup orchestration logic
│   ├── exporter.py                 # notion2md integration
│   ├── os_scheduler/               # Windows + Linux scheduler backends
│   └── ui/                         # Qt (Windows) and GTK (Linux) UIs
├── tests/                          # Unit tests
├── assets/                         # App icon/logo
├── packaging/
│   ├── common/notionsafe.desktop   # Shared Linux desktop entry
│   ├── copr/notionsafe.spec        # Fedora/COPR spec
│   └── aur/notionsafe/PKGBUILD     # Arch/AUR packaging files
├── pyproject.toml
├── requirements.txt
└── requirements-linux.txt
```

## Release Workflow

1. Update version in `pyproject.toml`.
2. Run tests locally (`pytest`).
3. Build source archive (`git archive` or release tarball flow).
4. Validate packaging files:
   - `packaging/copr/notionsafe.spec`
   - `packaging/aur/notionsafe/PKGBUILD`
5. Create GitHub release and attach source tarball.
6. Update checksums/version in AUR and rebuild COPR.

## Known Issues

- Windows `notionsafe` launcher can break if a virtualenv is moved across directories. Recreate the venv if you see a stale launcher path error.
- PyInstaller backup execution path has had historical instability around `notion2md`; verify packaged manual backup before tagging a release.

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
You can now run the application and test its functionality, including the `systemd` scheduler integration.

#### Running the GUI
```bash
python -m notebackup
```
The GTK or QT UI, based on your OS should launch.

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
