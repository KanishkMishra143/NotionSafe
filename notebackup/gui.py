import sys
import io
from PySide6.QtCore import Signal, QObject, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget
from notebackup import cli as backup_cli # Import the CLI main function

# Custom stream to redirect stdout to a Qt signal
class QtOutputStream(QObject, io.TextIOBase):
    new_text = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def write(self, text):
        self.new_text.emit(text)
        return len(text)

    def flush(self):
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NotionSafe")
        self.setGeometry(100, 100, 800, 600)

        # --- Widgets ---
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFontFamily("Courier")

        self.run_button = QPushButton("Run Backup")

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.log_output, 4) # Give more stretch to the log
        layout.addWidget(self.run_button, 1)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # --- Connections ---
        self.run_button.clicked.connect(self.run_backup)

        # --- Redirect stdout ---
        self.output_stream = QtOutputStream()
        self.output_stream.new_text.connect(self.append_text)
        sys.stdout = self.output_stream

        self.append_text("Welcome to NotionSafe. Click 'Run Backup' to start.\n")

    def append_text(self, text):
        cursor = self.log_output.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        self.log_output.ensureCursorVisible()

    def run_backup(self):
        self.run_button.setEnabled(False)
        self.log_output.clear()
        self.append_text("Starting backup process...\n")
        QApplication.processEvents() # Update the GUI

        try:
            backup_cli.main() # Run the main backup logic
            self.append_text("\nBackup process finished.\n")
        except Exception as e:
            self.append_text(f"\nAn error occurred: {e}\n")
        finally:
            self.run_button.setEnabled(True)
            QApplication.processEvents() # Update the GUI

    def closeEvent(self, event):
        # Restore stdout when the window closes
        sys.stdout = sys.__stdout__
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
