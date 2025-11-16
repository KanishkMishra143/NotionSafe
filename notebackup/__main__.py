# notebackup/__main__.py

import sys
import platform

def main():
    """
    Primary entry point for the NotionSafe application.
    Detects the operating system and launches the appropriate UI.
    """
    current_os = platform.system()

    if current_os == "Windows":
        print("Launching Qt UI for Windows...")
        try:
            from notebackup.ui import qt_ui
            qt_ui.main()
        except ImportError as e:
            print(f"Error: Failed to import Qt UI components. Make sure PySide6 is installed. Details: {e}", file=sys.stderr)
            sys.exit(1)
    elif current_os == "Linux":
        print("Launching GTK UI for Linux...")
        try:
            from notebackup.ui import gtk_ui
            gtk_ui.main()
        except ImportError as e:
            print(f"Error: Failed to import GTK UI components. Make sure PyGObject and its dependencies are installed. Details: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Error: Unsupported operating system '{current_os}'.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
