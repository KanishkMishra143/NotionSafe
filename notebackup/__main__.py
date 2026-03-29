# notebackup/__main__.py

import sys
import os
import platform
import argparse
import ctypes
from notebackup.logger import log

def hide_console():
    """Hides the console window on Windows."""
    if platform.system() == "Windows":
        # Get the handle to the console window
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        hWnd = kernel32.GetConsoleWindow()
        if hWnd:
            # Check if the console was started by this process or if we are attached to an existing one
            # If we were double-clicked, we want to hide it.
            # A simple heuristic: if no arguments (not --cli, not --gui, not --help) are provided, we hide it.
            user32.ShowWindow(hWnd, 0) # 0 = SW_HIDE

def main():
    """
    Primary entry point for the NotionSafe application.
    Distinguishes between CLI and GUI modes.
    """
    parser = argparse.ArgumentParser(description="NotionSafe: Secure local backups for your Notion workspace.", add_help=False)
    parser.add_argument('--gui', action='store_true', help='Force launch the GUI.')
    parser.add_argument('--cli', action='store_true', help='Force launch the CLI.')
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit.')
    
    # Peek at arguments to see if we should show help or default to GUI
    args, unknown = parser.parse_known_args()

    # Explicitly check for GUI-related admin flags to avoid falling into CLI mode
    is_admin_action = any('--run-as-admin' in arg for arg in sys.argv)
    
    # Define is_terminal to detect if we are running in a shell
    # On Windows, we check if stdin is a terminal to see if we were launched from a shell
    is_terminal = sys.stdin and sys.stdin.isatty()

    if args.help:
        parser.print_help()
        print("\nCLI Commands (when running in CLI mode):")
        print("  --config PATH    Path to the configuration file (default: ~/.noteback/config.yaml)")
        sys.exit(0)

    force_gui = args.gui or is_admin_action
    force_cli = args.cli or (len(unknown) > 0 and not force_gui)
    
    if force_cli:
        # CLI Mode
        from notebackup import cli
        # Re-parse with full CLI parser
        cli_parser = argparse.ArgumentParser(description="NotionSafe CLI")
        cli_parser.add_argument('--config', default='~/.noteback/config.yaml', help='Path to the configuration file.')
        cli_args = cli_parser.parse_args(unknown)
        
        log.info("Starting NotionSafe in CLI mode...")
        if not cli.main(config_path=cli_args.config):
            sys.exit(1)
        sys.exit(0)
    else:
        # GUI Mode (Default)
        # Hide console if we are not in a terminal and running as a frozen EXE
        if not is_terminal and getattr(sys, 'frozen', False):
            hide_console()
            
        current_os = platform.system()
        if current_os == "Windows":
            try:
                from notebackup.ui import qt_ui
                qt_ui.main()
            except ImportError as e:
                log.error(f"Error: Failed to import Qt UI components. Make sure PySide6 is installed. Details: {e}")
                sys.exit(1)
        elif current_os == "Linux":
            try:
                from notebackup.ui import gtk_ui
                gtk_ui.main()
            except ImportError as e:
                log.error(f"Error: Failed to import GTK UI components. Details: {e}")
                sys.exit(1)
        else:
            log.error(f"Error: Unsupported operating system '{current_os}'.")
            sys.exit(1)

if __name__ == "__main__":
    main()
