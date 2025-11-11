import sys
import logging
import os
import time
import yaml
import ctypes
from PySide6.QtCore import Signal, QObject, Qt, QThread
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QProgressBar, QLabel, QFrame, QHBoxLayout, QMessageBox, QWizard, QStyle
from PySide6.QtGui import QAction, QColor, QTextCursor, QIcon

from notebackup import cli
from notebackup.config_wizard import ConfigWizard
from notebackup.logger import log
from notebackup.scheduler import SchedulerThread
from notebackup import task_scheduler

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

    def __init__(self, config_path):
        super().__init__()
        self.config_path = config_path

    def run(self):
        try:
            cli.main(config_path=self.config_path, progress_callback=self.progress)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))



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

        # --- Widgets ---
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFontFamily("Courier")
        self.progress_bar = QProgressBar()
        self.run_button = QPushButton(self.style().standardIcon(QStyle.SP_MediaPlay), "Run Manual Backup")
        self.scheduled_backup_label = QLabel("Scheduled Backup Progress:")
        self.scheduled_backup_label.hide() # Initially hidden

        # --- Scheduler Controls ---
        scheduler_frame = QFrame()
        scheduler_frame.setFrameShape(QFrame.StyledPanel)
        scheduler_layout = QHBoxLayout(scheduler_frame)
        self.start_scheduler_button = QPushButton(self.style().standardIcon(QStyle.SP_MediaPlay), "Start Scheduler")
        self.stop_scheduler_button = QPushButton(self.style().standardIcon(QStyle.SP_MediaStop), "Stop Scheduler")
        self.next_run_label = QLabel("Next run: Not scheduled")
        scheduler_layout.addWidget(self.start_scheduler_button)
        scheduler_layout.addWidget(self.stop_scheduler_button)
        scheduler_layout.addWidget(self.next_run_label)
        self.stop_scheduler_button.setEnabled(False)

        # --- Task Scheduler Controls ---
        task_scheduler_frame = QFrame()
        task_scheduler_frame.setFrameShape(QFrame.StyledPanel)
        task_scheduler_layout = QHBoxLayout(task_scheduler_frame)
        self.install_task_button = QPushButton("Install Scheduled Task")
        self.uninstall_task_button = QPushButton("Uninstall Scheduled Task")
        task_scheduler_layout.addWidget(self.install_task_button)
        task_scheduler_layout.addWidget(self.uninstall_task_button)

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.log_output, 4)
        layout.addWidget(self.scheduled_backup_label) # Add the label
        layout.addWidget(self.progress_bar)
        layout.addWidget(scheduler_frame)
        layout.addWidget(task_scheduler_frame)
        layout.addWidget(self.run_button, 1)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # --- Connections ---
        self.run_button.clicked.connect(self.run_backup)
        self.start_scheduler_button.clicked.connect(self.start_scheduler)
        self.stop_scheduler_button.clicked.connect(self.stop_scheduler)
        self.install_task_button.clicked.connect(self.install_task)
        self.uninstall_task_button.clicked.connect(self.uninstall_task)

        # --- Logging ---
        self.log_handler = QTextEditLogHandler(self)
        self.log_handler.new_record.connect(self.append_text)
        log.addHandler(self.log_handler)

        self.scheduler_thread = None
        log.info("Welcome to NotionSafe. Click 'Run Manual Backup' to start a backup.")

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
        QMessageBox.information(self, "Help", "This application backs up your Notion workspace.\n\n- Use the 'Edit > Edit Configuration' menu to set up your Notion token and select pages/databases.\n- Click 'Run Manual Backup' to perform a one-time backup.\n- Use the scheduler controls to enable automatic backups.")

    def show_about(self):
        QMessageBox.about(self, "About NotionSafe", "NotionSafe v1.0\n\nA simple tool to back up your Notion workspace locally.")

    def show_config_wizard(self):
        wizard = ConfigWizard(self)
        wizard.exec()

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
        self.worker.start()

    def backup_finished(self):
        self.run_button.setEnabled(True)
        self.statusBar().showMessage('Backup complete', 5000)
        self.progress_bar.setValue(100)

    def backup_error(self, error_message):
        self.run_button.setEnabled(True)
        self.statusBar().showMessage('Backup failed!', 5000)
        log.error(f"An unexpected error occurred: {error_message}", exc_info=True)

    def start_scheduler(self):
        self.start_scheduler_button.setEnabled(False)
        self.stop_scheduler_button.setEnabled(True)
        self.statusBar().showMessage('Scheduler started')
        log.info("Starting scheduler...")

        config_path = os.path.expanduser("~/.noteback/config.yaml")
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            interval_hours = config['storage'].get('backup_frequency_hours', 24)
        except (FileNotFoundError, KeyError):
            log.warning("Could not read backup frequency from config. Defaulting to 24 hours.")
            interval_hours = 24

        self.scheduler_thread = SchedulerThread(self._scheduled_backup_job, interval_hours, config_path)
        self.scheduler_thread.status_changed.connect(self.append_text)
        self.scheduler_thread.error.connect(self.backup_error)
        self.scheduler_thread.next_run_time.connect(self.update_next_run_time)
        self.scheduler_thread.job_started.connect(self.scheduled_job_started)
        self.scheduler_thread.job_finished.connect(self.scheduled_job_finished)
        self.scheduler_thread.progress.connect(self.progress_bar.setValue)
        self.scheduler_thread.start()

    def stop_scheduler(self):
        if self.scheduler_thread:
            self.scheduler_thread.stop()
            self.scheduler_thread.wait()
        self.start_scheduler_button.setEnabled(True)
        self.stop_scheduler_button.setEnabled(False)
        self.statusBar().showMessage('Scheduler stopped')
        self.next_run_label.setText("Next run: Not scheduled") # Clear the label
        log.info("Scheduler stopped.")

    def update_next_run_time(self, next_run): # Re-add this method
        self.next_run_label.setText(f"Next run: {next_run}")

    def install_task(self):
        log.info("Installing scheduled task...")
        config_path = os.path.expanduser("~/.noteback/config.yaml")
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            interval_hours = config['storage'].get('backup_frequency_hours', 24)
        except (FileNotFoundError, KeyError):
            log.warning("Could not read backup frequency from config. Defaulting to 24 hours.")
            interval_hours = 24
            
        success, message = task_scheduler.create_task(interval_hours)
        if success:
            QMessageBox.information(self, "Task Scheduler", message)
        else:
            QMessageBox.critical(self, "Task Scheduler", message)
        log.info(message)

    def uninstall_task(self):
        log.info("Uninstalling scheduled task...")
        success, message = task_scheduler.delete_task()
        if success:
            QMessageBox.information(self, "Task Scheduler", message)
        else:
            QMessageBox.critical(self, "Task Scheduler", message)
        log.info(message)

    def closeEvent(self, event):
        self.stop_scheduler()
        event.accept()

def main():
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
