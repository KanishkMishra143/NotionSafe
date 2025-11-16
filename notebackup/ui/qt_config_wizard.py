import sys
import os
import yaml
import keyring
import notion_client
from PySide6.QtWidgets import QWizard, QWizardPage, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QFileDialog, QPushButton, QListWidget, QListWidgetItem, QComboBox, QMessageBox, QApplication
from PySide6.QtCore import Qt
from ..auth import SERVICE_ID
from ..logger import log

class ConfigWizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("NotionSafe Configuration Wizard")
        self.setStyleSheet("""
            QWizard, QWizardPage {
                background-color: white;
            } 
            QLabel, QCheckBox {
                color: black;
            }
        """)

        self.addPage(WelcomePage())
        self.addPage(StoragePage())
        self.addPage(NotionApiPage())
        self.addPage(NotionContentPage())
        self.addPage(SchedulePage())
        self.addPage(SummaryPage())

    def accept(self):
        """Called when the user clicks Finish. Gathers all data and saves the config."""
        local_enabled = self.page(1).field("local_check")
        local_path = self.page(1).field("local_path_edit") if local_enabled else ""
        external_enabled = self.page(1).field("external_check")
        external_path = self.page(1).field("external_path_edit") if external_enabled else ""
        git_enabled = self.page(1).field("git_check")
        git_url = self.page(1).field("git_url_edit") if git_enabled else ""
        token = self.page(2).field("token_edit")
        keyring.set_password(SERVICE_ID, "notion_token", token)
        page_ids = self.page(3).get_selected_ids(self.page(3).page_list)
        db_ids = self.page(3).get_selected_ids(self.page(3).db_list)
        frequency_map = {"Daily": 24, "Weekly": 168, "Monthly": 720}
        frequency = self.page(4).field("frequency_combo")
        backup_frequency_hours = frequency_map.get(frequency, 24)

        config_data = {
            "notion": {"page_ids": page_ids, "database_ids": db_ids},
            "storage": {
                "local_path": os.path.expanduser(local_path),
                "backup_frequency_hours": backup_frequency_hours,
                "external_drive": {"enabled": external_enabled, "path": os.path.expanduser(external_path)},
                "git": {"enabled": git_enabled, "remote_url": git_url, "remote_name": "origin"},
            },
        }

        config_dir = os.path.expanduser("~/.noteback")
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, "config.yaml")

        try:
            with open(config_path, "w") as f:
                yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)
            log.info(f"Configuration successfully saved to {config_path}")
            QMessageBox.information(self, "Success", f"Configuration saved to {config_path}")
            super().accept()
        except IOError as e:
            log.error(f"Failed to write config file: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to write config file: {e}")


class WelcomePage(QWizardPage): # Page 0
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Welcome to NotionSafe")
        self.setSubTitle("This wizard will guide you through creating your backup configuration file (config.yaml).")
        self.setLayout(QVBoxLayout())

class StoragePage(QWizardPage): # Page 1
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Storage Options")

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # --- Local Backup ---
        self.local_check = QCheckBox("Enable Local Backup")
        self.local_check.setChecked(True)
        layout.addWidget(self.local_check)
        self.registerField("local_check", self.local_check)

        self.local_path_edit = QLineEdit()
        self.local_path_edit.setPlaceholderText("e.g., ~/Documents/NotionBackups")
        layout.addWidget(self.local_path_edit)
        self.registerField("local_path_edit", self.local_path_edit)

        local_browse_button = QPushButton("Browse...")
        layout.addWidget(local_browse_button)

        # --- External Drive ---
        self.external_check = QCheckBox("Enable External Drive Copy")
        layout.addWidget(self.external_check)
        self.registerField("external_check", self.external_check)

        self.external_path_edit = QLineEdit()
        self.external_path_edit.setPlaceholderText("e.g., /Volumes/MyUSB/NotionBackups")
        self.external_path_edit.setEnabled(False)
        layout.addWidget(self.external_path_edit)
        self.registerField("external_path_edit", self.external_path_edit)

        external_browse_button = QPushButton("Browse...")
        layout.addWidget(external_browse_button)

        # --- Git Backup ---
        self.git_check = QCheckBox("Enable Git Versioning")
        layout.addWidget(self.git_check)
        self.registerField("git_check", self.git_check)

        self.git_url_edit = QLineEdit()
        self.git_url_edit.setPlaceholderText("e.g., git@github.com:user/repo.git")
        self.git_url_edit.setEnabled(False)
        layout.addWidget(self.git_url_edit)
        self.registerField("git_url_edit", self.git_url_edit)

        # --- Connections ---
        self.external_check.toggled.connect(self.external_path_edit.setEnabled)
        self.git_check.toggled.connect(self.git_url_edit.setEnabled)
        local_browse_button.clicked.connect(self.browse_local_path)
        external_browse_button.clicked.connect(self.browse_external_drive)

    def browse_local_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if path:
            self.local_path_edit.setText(path)

    def browse_external_drive(self):
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if path:
            self.external_path_edit.setText(path)

class NotionApiPage(QWizardPage): # Page 2
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Notion Integration")

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        layout.addWidget(QLabel("Enter your Notion Integration Token:"))
        self.token_edit = QLineEdit()
        self.token_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.token_edit)

        self.registerField("token_edit*", self.token_edit)

    def initializePage(self):
        existing_token = keyring.get_password(SERVICE_ID, "notion_token")
        if existing_token:
            self.token_edit.setText(existing_token)

class NotionContentPage(QWizardPage): # Page 3
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Content Selection")
        self.setSubTitle("Fetch and select the pages and databases you want to back up.")

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.fetch_button = QPushButton("Fetch Pages & Databases")
        layout.addWidget(self.fetch_button)

        layout.addWidget(QLabel("Pages:"))
        self.page_list = QListWidget()
        layout.addWidget(self.page_list)

        layout.addWidget(QLabel("Databases:"))
        self.db_list = QListWidget()
        layout.addWidget(self.db_list)

        self.fetch_button.clicked.connect(self.fetch_content)

    def fetch_content(self):
        token = self.wizard().page(2).field("token_edit")
        if not token:
            log.warning("Notion API token is missing.")
            QMessageBox.warning(self, "Missing Token", "Please enter a Notion API token on the previous page.")
            return

        try:
            self.fetch_button.setText("Fetching...")
            self.fetch_button.setEnabled(False)
            QApplication.processEvents()

            notion = notion_client.Client(auth=token)
            results = notion.search()["results"]
            
            self.page_list.clear()
            self.db_list.clear()

            for result in results:
                item_id = result.get("id")
                if result["object"] == "page":
                    title_list = result.get("properties", {}).get("title", {}).get("title", [])
                    title = title_list[0].get("plain_text", item_id) if title_list else item_id
                    item = QListWidgetItem(title)
                    item.setData(Qt.UserRole, item_id)
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(Qt.Unchecked)
                    self.page_list.addItem(item)
                elif result["object"] == "database":
                    title_list = result.get("title", [])
                    title = title_list[0].get("plain_text", item_id) if title_list else item_id
                    item = QListWidgetItem(title)
                    item.setData(Qt.UserRole, item_id)
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(Qt.Unchecked)
                    self.db_list.addItem(item)
            log.info(f"Successfully fetched {self.page_list.count()} pages and {self.db_list.count()} databases from Notion.")

        except Exception as e:
            log.error(f"Failed to fetch from Notion: {e}", exc_info=True)
            QMessageBox.critical(self, "API Error", f"Failed to fetch from Notion: {e}")
        finally:
            self.fetch_button.setText("Fetch Pages & Databases")
            self.fetch_button.setEnabled(True)

    def get_selected_ids(self, list_widget):
        return [list_widget.item(i).data(Qt.UserRole) for i in range(list_widget.count()) if list_widget.item(i).checkState() == Qt.Checked]

class SchedulePage(QWizardPage): # Page 4
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Backup Frequency")

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        layout.addWidget(QLabel("How often should backups run?"))
        self.frequency_combo = QComboBox()
        self.frequency_combo.addItems(["Daily", "Weekly", "Monthly"])
        layout.addWidget(self.frequency_combo)

        self.registerField("frequency_combo", self.frequency_combo, "currentText")

class SummaryPage(QWizardPage): # Page 5
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Configuration Complete")
        self.setSubTitle("Click 'Finish' to save your configuration.")
        self.setLayout(QVBoxLayout())

# Main execution logic remains the same...