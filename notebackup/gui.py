import sys
import logging
import os
import time
import yaml
import ctypes
from PySide6.QtCore import Signal, QObject, Qt, QThread
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QProgressBar, QLabel, QFrame, QHBoxLayout, QMessageBox, QWizard, QStyle, QTabWidget
from PySide6.QtGui import QAction, QColor, QTextCursor, QIcon

from notebackup import cli
from notebackup.config_wizard import ConfigWizard
from notebackup.logger import log
from notebackup.scheduler import SchedulerThread
from notebackup.os_scheduler import get_scheduler
from notebackup.core import BackupRunner
from notebackup.cli import InvalidNotionTokenError

# 1. Custom logging handler that emits a Qt signal
class QTextEditLogHandler(logging.Handler, QObject):
    new_record = Signal(str)

    def __init__(self, parent):
        super().__init__()
        QObject.__init__(self)
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

    def emit(self, record):
        msg = self.format(record)
        self.new_record.emit(msg)

class Worker(QThread):
    progress = Signal(int)
    finished = Signal()
    error = Signal(str)
    invalid_token_error = Signal() # New signal for invalid token

    def __init__(self, config_path):
        super().__init__()
        self.config_path = config_path

    def run(self):
        runner = BackupRunner(self.config_path)
        runner.run(
            progress_callback=self.progress.emit,
            finished_callback=self.finished.emit,
            error_callback=self.error.emit,
            invalid_token_callback=self.invalid_token_error.emit
        )



def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NotionSafe")
        self.setWindowIcon(QIcon('assets/logo.png'))
        self.setGeometry(100, 100, 800, 600)

        # --- Menu Bar ---
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        edit_menu = menu_bar.addMenu("&Edit")
        help_menu = menu_bar.addMenu("&Help")

        exit_action = QAction(self.style().standardIcon(QStyle.SP_DialogCloseButton), "&Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_config_action = QAction(self.style().standardIcon(QStyle.SP_FileDialogDetailedView), "Edit &Configuration", self)
        edit_config_action.triggered.connect(self.show_config_wizard)
        edit_menu.addAction(edit_config_action)

        help_action = QAction(self.style().standardIcon(QStyle.SP_DialogHelpButton), "&Help", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        about_action = QAction(self.style().standardIcon(QStyle.SP_MessageBoxInformation), "&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # --- Status Bar ---
        self.statusBar().showMessage('Ready')

        # --- Widgets that are part of the main layout ---
        self.scheduled_backup_label = QLabel("Scheduled Backup Progress:")
        self.scheduled_backup_label.hide() # Initially hidden
        self.progress_bar = QProgressBar()
        self.run_button = QPushButton(self.style().standardIcon(QStyle.SP_MediaPlay), "Run Manual Backup")

        # --- Tabbed Interface ---
        self.tabs = QTabWidget()
        self.log_tab = QWidget()
        self.scheduler_tab = QWidget()

        self.tabs.addTab(self.log_tab, "Log")
        self.tabs.addTab(self.scheduler_tab, "Scheduler")

        # --- Log Tab Layout ---
        log_layout = QVBoxLayout(self.log_tab)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFontFamily("Courier")
        log_layout.addWidget(self.log_output)

        # --- Scheduler Tab Layout ---
        scheduler_layout = QVBoxLayout(self.scheduler_tab)
        scheduler_layout.setAlignment(Qt.AlignTop)

        title_label = QLabel("OS-Native Backup Scheduler")
        font = title_label.font()
        font.setBold(True)
        font.setPointSize(12)
        title_label.setFont(font)

        description_label = QLabel("This scheduler uses the operating system's native task scheduler (Windows Task Scheduler or systemd on Linux) to run backups automatically in the background, even if this application is closed.")
        description_label.setWordWrap(True)

        self.scheduler_status_label = QLabel("Status: Unknown")
        self.scheduler_toggle_button = QPushButton("Enable Scheduled Backup")
        self.backup_frequency_label = QLabel("Backup Frequency: Unknown")

        scheduler_layout.addWidget(title_label)
        scheduler_layout.addWidget(description_label)
        scheduler_layout.addSpacing(20)
        
        status_layout = QHBoxLayout()
        status_layout.addWidget(self.scheduler_status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.backup_frequency_label)
        scheduler_layout.addLayout(status_layout)

        scheduler_layout.addWidget(self.scheduler_toggle_button)
        scheduler_layout.addStretch()

        # --- Main Layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.tabs, 4) # Add tabs
        layout.addWidget(self.scheduled_backup_label)
        layout.addWidget(self.progress_bar)
        # layout.addWidget(scheduler_frame) # In-app scheduler, not OS task
        layout.addWidget(self.run_button, 1)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # --- Connections ---
        self.run_button.clicked.connect(self.run_backup)
        # self.start_scheduler_button.clicked.connect(self.start_scheduler)
        # self.stop_scheduler_button.clicked.connect(self.stop_scheduler)
        self.scheduler_toggle_button.clicked.connect(self.toggle_schedule)

        # --- Logging ---
        self.log_handler = QTextEditLogHandler(self)
        self.log_handler.new_record.connect(self.append_text)
        log.addHandler(self.log_handler)

        self.scheduler_thread = None
        self.scheduler = get_scheduler()
        log.info("Welcome to NotionSafe. Click 'Run Manual Backup' to start a backup.")

        self.update_scheduler_status() # Initial check

    def _scheduled_backup_job(self, config_path, progress_callback):
        """
        This method is called by the scheduler thread to perform a backup.
        """
        try:
            cli.main(config_path=config_path, progress_callback=progress_callback)
        except Exception as e:
            log.error(f"Scheduled backup failed: {e}", exc_info=True)

    def scheduled_job_started(self):
        self.log_output.clear()
        self.progress_bar.setValue(0)
        self.scheduled_backup_label.show()

    def scheduled_job_finished(self):
        self.scheduled_backup_label.hide()

    def show_help(self):
        QMessageBox.information(self, "Help", "This application backs up your Notion workspace.\n\n- Use the 'Edit > Edit Configuration' menu to set up your Notion token and select pages/databases.\n- Click 'Run Manual Backup' to perform a one-time backup.\n- Use the 'Scheduler' tab to enable automatic background backups.")

    def show_about(self):
        QMessageBox.about(self, "About NotionSafe", "NotionSafe v1.0\n\nA simple tool to back up your Notion workspace locally.")

    def show_config_wizard(self):
        wizard = ConfigWizard(self)
        wizard.exec()
        self.update_scheduler_status() # Update frequency after config change

    def append_text(self, text):
        if "ERROR" in text:
            self.log_output.setTextColor(QColor("red"))
            self.statusBar().showMessage('Error occurred', 5000)
        elif "WARNING" in text:
            self.log_output.setTextColor(QColor("orange"))
            self.statusBar().showMessage('Warning', 5000)
        else:
            self.log_output.setTextColor(QColor("black"))

        cursor = self.log_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text + '\n')
        self.log_output.ensureCursorVisible()

    def run_backup(self):
        self.run_button.setEnabled(False)
        self.statusBar().showMessage('Running backup...')
        self.log_output.clear()
        self.progress_bar.setValue(0)
        log.info("Starting manual backup process...")

        config_path = os.path.expanduser("~/.noteback/config.yaml")
        self.worker = Worker(config_path)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.backup_finished)
        self.worker.error.connect(self.backup_error)
        self.worker.invalid_token_error.connect(self.handle_invalid_token_error) # Connect new signal
        self.worker.start()

    def backup_finished(self):
        self.run_button.setEnabled(True)
        self.statusBar().showMessage('Backup complete', 5000)
        self.progress_bar.setValue(100)

    def backup_error(self, error_message):
        self.run_button.setEnabled(True)
        self.statusBar().showMessage('Backup failed!', 5000)
        log.error(f"An unexpected error occurred: {error_message}", exc_info=True)

    def handle_invalid_token_error(self):
        self.run_button.setEnabled(True)
        self.statusBar().showMessage('Backup failed: Invalid Notion Token!', 5000)
        QMessageBox.critical(self, "Invalid Notion Token",
                             "The Notion API token is invalid or unauthorized.\n"
                             "Please re-run the Configuration Wizard to update your token.")
        self.show_config_wizard() # Prompt to re-run wizard

    def update_scheduler_status(self):
        is_scheduled = self.scheduler.is_scheduled()
        if is_scheduled:
            self.scheduler_status_label.setText("Status: <font color='green'><b>Enabled</b></font>")
            self.scheduler_toggle_button.setText("Disable Scheduled Backup")
        else:
            self.scheduler_status_label.setText("Status: <font color='red'><b>Disabled</b></font>")
            self.scheduler_toggle_button.setText("Enable Scheduled Backup")

        # Update backup frequency display
        config_path = os.path.expanduser("~/.noteback/config.yaml")
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            interval_hours = config['storage'].get('backup_frequency_hours', 24)
            self.backup_frequency_label.setText(f"Backup Frequency: Every {interval_hours} hours")
        except (FileNotFoundError, KeyError):
            self.backup_frequency_label.setText("Backup Frequency: Unknown")

    def toggle_schedule(self):
        is_scheduled = self.scheduler.is_scheduled()
        action = "delete-task" if is_scheduled else "create-task"

        if not is_admin():
            log.warning("Admin privileges required. Attempting to re-launch with UAC prompt...")
            try:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'-m notebackup.gui --run-as-admin {action}', None, 1)
                # The main app doesn't exit, it just triggers the admin process
                # We can't reliably know the outcome of the UAC prompt here, so we just log and update the UI optimistically after a delay
                # A more robust solution might involve IPC, but this is simpler.
                log.info("A UAC prompt should now be visible. Please approve it to continue.")
                # We can't immediately update the status, as the user might cancel the UAC prompt.
                # We will let the user see the result of their action. A manual refresh could be added.
                return
            except Exception as e:
                log.error(f"Failed to re-launch with admin rights: {e}")
                QMessageBox.critical(self, "Elevation Error", f"Failed to request administrator privileges: {e}")
                return

        # This code runs if we are already admin, or if the above call is modified to run this part
        log.info(f"Running scheduler action as admin: {action}")
        if action == "delete-task":
            success, message = self.scheduler.delete()
        else: # create-task
            config_path = os.path.expanduser("~/.noteback/config.yaml")
            try:
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                interval_hours = config['storage'].get('backup_frequency_hours', 24)
            except (FileNotFoundError, KeyError):
                log.warning("Could not read backup frequency from config. Defaulting to 24 hours.")
                interval_hours = 24
            success, message = self.scheduler.create(interval_hours)

        if success:
            QMessageBox.information(self, "Task Scheduler", message)
            log.info(message)
        else:
            QMessageBox.critical(self, "Task Scheduler", f"An error occurred: {message}")
            log.error(message)
        
        self.update_scheduler_status()

    def closeEvent(self, event):
        # self.stop_scheduler()
        event.accept()

def main():
    # Part of the UAC elevation process
    if '--run-as-admin' in sys.argv:
        action_index = sys.argv.index('--run-as-admin') + 1
        if action_index < len(sys.argv):
            action = sys.argv[action_index]
            scheduler = get_scheduler()
            if action == "create-task":
                config_path = os.path.expanduser("~/.noteback/config.yaml")
                try:
                    with open(config_path, 'r') as f:
                        config = yaml.safe_load(f)
                    interval_hours = config['storage'].get('backup_frequency_hours', 24)
                except (FileNotFoundError, KeyError):
                    interval_hours = 24
                scheduler.create(interval_hours)
            elif action == "delete-task":
                scheduler.delete()
        sys.exit(0) # The admin task is done, exit

    app = QApplication(sys.argv)

    config_path = os.path.expanduser("~/.noteback/config.yaml")
    if not os.path.exists(config_path):
        wizard = ConfigWizard()
        if wizard.exec() != QWizard.Accepted:
            sys.exit(0)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
