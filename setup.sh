#!/bin/bash
set -euo pipefail

# --- NotionSafe Installer ---
# This script sets up the NotionSafe environment on Linux.

# --- Helper Functions ---
print_step() {
    echo -e "\n\e[1;34m>> $1\e[0m"
}

detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    else
        echo "unknown"
    fi
}

install_packages_debian() {
    print_step "Installing packages for Debian/Ubuntu..."
    sudo apt-get update
    sudo apt-get install -y git git-lfs rsync python3 python3-venv python3-dev build-essential libssl-dev libffi-dev
}

install_packages_fedora() {
    print_step "Installing packages for Fedora/RHEL..."
    sudo dnf install -y git git-lfs rsync python3 python3-devel gcc-c++ openssl-devel libffi-devel
}

setup_python_venv() {
    print_step "Setting up Python virtual environment..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo "Created Python virtual environment in 'venv/'."
    else
        echo "Virtual environment 'venv/' already exists."
    fi
    
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "Python dependencies installed."
}

init_git() {
    print_step "Initializing Git repository..."
    if [ ! -d ".git" ]; then
        git init
        git lfs install
        git branch -M main
        # Create backup branch
        git checkout -b backup
        git checkout main
        echo "Git repository initialized and LFS installed."
    else
        echo "Git repository already exists."
    fi
    
    # Configure LFS tracking
    git lfs track "*.png" "*.jpg" "*.jpeg" "*.gif" "*.mp4" "*.pdf" "*.mov" "*.zip" "*.tar.gz" "*.gz"
    git add .gitattributes
    echo "Configured Git LFS tracking."
}

run_bootstrap() {
    print_step "Running bootstrap..."
    if [ -z "${NOTION_TOKEN:-}" ]; then
        echo "Warning: NOTION_TOKEN environment variable is not set."
        echo "The bootstrap run will likely fail to authenticate."
    fi

    # Create a default config if it doesn't exist
    if [ ! -f ~/.noteback/config.yaml ]; then
        mkdir -p ~/.noteback
        cp examples/backup_config.yaml ~/.noteback/config.yaml
        echo "Created default config at ~/.noteback/config.yaml. Please edit it with your Page/DB IDs."
    fi

    # Run the backup script
    source venv/bin/activate
    python scripts/backup_runner.py
}

print_final_checklist() {
    print_step "Setup Complete! Next Steps:"
    echo "1.  ✅ Share Notion pages/databases with your integration."
    echo "2.  ✅ Set NOTION_TOKEN environment variable or run the app once to save it to keyring:"
    echo "       export NOTION_TOKEN='your_secret_token'"
    echo "3.  ✅ Edit your configuration file with Page/DB IDs:"
    echo "       nano ~/.noteback/config.yaml"
    echo "4.  ✅ Configure your Git remote URL in the config file."
    echo "5.  ✅ Run a test backup:"
    echo "       source venv/bin/activate && python scripts/backup_runner.py"
    echo "6.  ✅ (Optional) Install the systemd timer for automatic backups:"
    echo "       source venv/bin/activate && python scripts/backup_runner.py --install-timer"
    echo "7.  ✅ (Optional) Or, get instructions for a cron job:"
    echo "       source venv/bin/activate && python scripts/backup_runner.py --cron-job"
}

# --- Main Execution ---
main() {
    if [ "$#" -eq 0 ]; then
        echo "Usage: $0 --install | --bootstrap"
        exit 1
    fi

    if [ "$1" == "--install" ]; then
        DISTRO=$(detect_distro)
        case "$DISTRO" in
            ubuntu|debian)
                install_packages_debian
                ;;
            fedora|rhel|centos)
                install_packages_fedora
                ;;
            *)
                echo "Unsupported Linux distribution: $DISTRO"
                echo "Please install the required packages manually: git, git-lfs, rsync, python3, python3-venv, python3-dev, build-tools."
                ;;
        esac
        
        setup_python_venv
        init_git
        print_final_checklist

    elif [ "$1" == "--bootstrap" ]; then
        run_bootstrap
    else
        echo "Invalid argument. Use --install or --bootstrap."
        exit 1
    fi
}

main "$@"
