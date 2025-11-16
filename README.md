# NotionSafe: Your Notion Workspace Backup Tool

NotionSafe is a cross-platform desktop application built with Python and PySide6 to create secure, local backups of your Notion workspaces. It provides a robust, versioned backup solution with both a graphical user interface (GUI) and a command-line interface (CLI).

![NotionSafe Logo](./assets/logo.png)

## Features

- **Cross-Platform GUI**: An easy-to-use graphical interface for configuration and backups, built with PySide6 to run on Windows, macOS, and Linux.
- **Configuration Wizard**: A simple, step-by-step wizard to get you started quickly.
- **OS-level Scheduled Backups**: Easily set up and manage automatic backups using your operating system's native task scheduler directly from the GUI.
- **Robust Git Backups**: Automatically backs up your workspace to a Git repository with a unique two-branch strategy:
    - `history` branch: Contains a complete, versioned history of every snapshot.
    - `master` branch: Always reflects the content of the very latest backup.
- **Multiple Sync Targets**: Store your backups in a local folder, copy them to an external drive, and push them to a remote Git repository.
- **Secure Token Storage**: Your Notion API token is stored securely in your operating system's native keyring.
- **Comprehensive Test Suite**: A full suite of `pytest` tests ensures application stability and reliability.

## Installation and Usage

### 1. Prerequisites
- Python 3.10 or newer.

### 2. Installation
Clone the repository and install the required dependencies.

```bash
git clone https://github.com/Gfreak412/notionsafe.git
cd notionsafe

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

You can configure NotionSafe using the GUI (recommended) or by creating the configuration file manually.

#### GUI (Recommended)
Run the GUI application. It will detect that you have no configuration and automatically launch the setup wizard.

```bash
python -m notebackup.gui
```
The wizard will guide you through:
1.  Setting your Notion API token.
2.  Choosing a local directory for your backups.
3.  Optionally, configuring a Git repository for versioned backups.
4.  Optionally, configuring an external drive to copy backups to.

#### Manual Configuration
1. Create a configuration file at `~/.noteback/config.yaml` (on Linux/macOS) or `C:\Users\<YourUser>\.noteback\config.yaml` (on Windows).
2. Copy the contents of `examples/backup_config.yaml` into your new file and edit the values to match your setup.

### 4. Running a Backup

#### From the GUI
If you have the GUI open, simply click the **"Run Manual Backup"** button to perform a one-time backup. You can view the progress in the log viewer window.

For automatic backups, use the **"Install Scheduled Task"** and **"Uninstall Scheduled Task"** buttons. The backup frequency can be configured in your `~/.noteback/config.yaml` file under the `storage` section (e.g., `backup_frequency_hours: 24`).

#### From the Command Line
To run a backup from the command line, execute the `cli` module:
```bash
python -m notebackup.cli
```

## 5. Troubleshooting and FAQs

### Q: A CMD window still pops up when the scheduled task runs!
**A:** This is a common issue with Windows Task Scheduler. Even when using `pythonw.exe` or other silent launchers, the Task Scheduler might still force a console window to appear due to its default settings.

**Resolution:** You need to manually adjust a setting within the Task Scheduler GUI:
1.  **Open Task Scheduler:** Search for "Task Scheduler" in the Windows Start Menu.
2.  **Locate the Task:** Navigate to `Task Scheduler Library` and find `NotionSafeBackup`.
3.  **Access Task Properties:** Right-click on `NotionSafeBackup` and select `Properties`.
4.  **Check "General" Tab:**
    *   Under "Security options", ensure **"Run whether user is logged on or not"** is selected.
    *   If you change this, you will be prompted to enter the password for the user account under which the task will run. This is necessary for the task to run silently in the background.
    *   Also, ensure **"Run with highest privileges"** is checked.
5.  Click `OK` to save changes.

### Q: The scheduled task seems to be stuck in a loop or running too frequently.
**A:** This usually happens if the task is configured to restart on failure, and the backup script is encountering an error.

**Resolution:** Check the task's restart settings:
1.  **Open Task Scheduler** and locate `NotionSafeBackup` (as above).
2.  **Access Task Properties** and go to the `Settings` tab.
3.  **"If the task fails, restart every:"**:
    *   **Recommendation:** Uncheck this box if you don't want the task to restart automatically on failure.
    *   **Alternative:** If restarts are desired, set the interval to a very long period (e.g., `1 day`) and set "Attempt to restart up to:" to a low number (e.g., `1` or `2`).
4.  Click `OK` to save changes.

## Development

- **Linting**: `flake8 .` and `black .`
- **Testing**: `pytest`

## Project Structure

```
.
├── notebackup/
│   ├── __init__.py
│   ├── auth.py
│   ├── cli.py
│   ├── config_wizard.py
│   ├── exporter.py
│   ├── fs_layout.py
│   ├── gitops.py
│   ├── gui.py
│   ├── logger.py
│   ├── notion_api.py
│   ├── scheduler.py
│   ├── storage.py
│   └── task_scheduler.py
├── tests/
│   ├── test_auth.py
│   ├── test_cli.py
│   └── ... (and other tests)
├── assets/
│   └── logo.png
├── examples/
│   └── backup_config.yaml
├── .gitignore
├── pyproject.toml
└── requirements.txt
```

---
## Linux Development Guide (Fedora)

This guide provides a comprehensive, step-by-step process for setting up a development environment for NotionSafe on a bare-metal Fedora installation. A bare-metal or full VM environment is required to properly test native Linux features like `systemd` timers.



### Step 1: Update Your System
Before installing new packages, it's always good practice to ensure your system is up-to-date.
```bash
sudo dnf update
sudo dnf install python3.11-devel gtk4-devel gobject-introspection-devel cairo-gobject-devel gnome-keyring
python3.11 -m pip install -r requirements-linux.txt 
python3.11 -m pip install pygobject
```

### Step 2: Install Core Build Dependencies
These packages are essential for compiling Python C-extensions that many libraries rely on.
```bash
sudo dnf install gcc python3-devel
```
-   `gcc`: The GNU Compiler Collection, used to compile C code.
-   `python3-devel`: Includes the header files needed to build Python extensions.

### Step 3: Install GUI Dependencies
NotionSafe uses GTK4 for its user interface on Linux. These packages provide the necessary libraries and introspection data for the Python bindings.
```bash
sudo dnf install gtk4-devel gobject-introspection-devel cairo-gobject-devel
```
-   `gtk4-devel`: Development files for the GTK4 toolkit.
-   `gobject-introspection-devel`: Allows Python to dynamically interact with C libraries (like GTK) through `PyGObject`.
-   `cairo-gobject-devel`: Development files for Cairo, a 2D graphics library used by GTK.

### Step 4: Install Backend Service Dependencies
These packages support key backend features like secure credential storage and Git integration.
```bash
sudo dnf install libsecret-devel dotnet-runtime-6.0
```
-   `libsecret-devel`: Required by the `keyring` library to securely store the Notion API token in the GNOME Keyring or other system secret services.
-   `dotnet-runtime-6.0`: A dependency for the recommended `git-credential-manager`.

### Step 5: Clone the Application Repository
Clone the source code from GitHub to your local machine.
```bash
git clone https://github.com/Gfreak412/notionsafe.git
cd notionsafe
```

### Step 6: Set Up a Python Virtual Environment
A virtual environment is a self-contained directory that holds a specific Python interpreter and its own set of installed packages. This is a critical best practice to avoid conflicts between projects.

```bash
# Create a directory named 'venv' for the environment
python3 -m venv venv

# Activate the environment. Your shell prompt should change to indicate it's active.
source venv/bin/activate
```
To deactivate the environment later, simply run `deactivate`.

### Step 7: Install Python Dependencies
Install all the required Python libraries listed in the requirements file for Linux.
```bash
pip install -r requirements-linux.txt
```
**Verification:** You can run `pip list` to see all the packages that were installed into your virtual environment.

### Step 8: Install NotionSafe in Editable Mode
This is the final step to make the application runnable. Installing in "editable" mode (`-e`) means that the installation links directly to your source code. Any edits you make to the `.py` files are immediately effective when you run the application, with no need to re-install.

```bash
pip install -e .
```
This command reads the `pyproject.toml` file and creates a runnable command `notionsafe` in your virtual environment's `bin` directory.

### Step 9: Configure Git Credentials (Recommended)
For a seamless experience pushing to a remote Git repository (especially with 2FA), it is recommended to use Git Credential Manager (GCM). GCM securely stores your Personal Access Token (PAT) in the system keyring.

```bash
# Enable the third-party Copr repository for GCM
sudo dnf copr enable matthickford/git-credential-manager

# Install the package
sudo dnf install git-credential-manager

# Configure Git to use GCM as its credential helper
git-credential-manager-core configure
```
The first time you `git push` to a private repository, you will be prompted for your username and password. Use your PAT as the password.

### Step 10: Run and Test the Application

#### Running the GUI
With the virtual environment still active, you can now run the application using the command created in Step 8:
```bash
notionsafe
```
The GTK user interface should launch. The first time it runs, it will prompt you to go through the configuration wizard.

#### Testing the Systemd Scheduler
The primary reason for using a bare-metal Fedora install is to test the native scheduler.
1.  Run the application (`notionsafe`) and complete the configuration wizard, ensuring you have a valid backup path.
2.  Navigate to the **Scheduler** tab.
3.  Click the **Enable Scheduled Backup** button. The application will create and install `systemd` timer and service files in `~/.config/systemd/user/`.
4.  You can verify the status of the timer and service using the following commands:
    ```bash
    # Check the status of the timer
    systemctl --user status notionsafe-backup.timer

    # Check the status of the service it triggers
    systemctl --user status notionsafe-backup.service

    # List all user timers to see when it's scheduled to run next
    systemctl --user list-timers
    ```

### Development FAQs

#### Q: Why can't I test `systemd` timers or `cron` jobs in WSL?
**A:** The Windows Subsystem for Linux (WSL), particularly WSL2, does not use a traditional Linux init system like `systemd`. Instead, it uses its own init process to manage the lifecycle of the Linux environment. `systemd` is the core service manager on modern Linux distributions like Fedora, responsible for running services, timers, and other background tasks. Since the `systemd` daemon is not running in WSL, you cannot create, enable, or test `systemd` timers. This makes a bare-metal Linux installation or a full virtual machine (like with VirtualBox or VMware) necessary for developing and testing features that rely on native system services.
