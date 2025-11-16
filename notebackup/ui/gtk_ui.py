# notebackup/ui/gtk_ui.py

import sys
import logging
import os
import threading
import yaml
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GLib, Gio
from ..logger import log
from ..core import BackupRunner
from ..cli import InvalidNotionTokenError
from ..os_scheduler import get_scheduler
from .gtk_config_wizard import GtkConfigWizard

class GtkLogHandler(logging.Handler):
    def __init__(self, text_buffer):
        super().__init__()
        self.buffer = text_buffer
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.setFormatter(formatter)

    def emit(self, record):
        msg = self.format(record) + '\n'
        GLib.idle_add(self.add_message, msg)

    def add_message(self, msg):
        end_iter = self.buffer.get_end_iter()
        self.buffer.insert(end_iter, msg, -1)
        return False

class Worker(threading.Thread):
    def __init__(self, config_path, callbacks):
        super().__init__()
        self.config_path = config_path
        self.callbacks = callbacks

    def run(self):
        runner = BackupRunner(self.config_path)
        runner.run(
            progress_callback=self.callbacks['progress'],
            finished_callback=self.callbacks['finished'],
            error_callback=self.callbacks['error'],
            invalid_token_callback=self.callbacks['invalid_token']
        )

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(800, 600)
        self.set_title("NotionSafe (GTK)")

        # Define action for the menu item
        action = Gio.SimpleAction.new("show_config_wizard", None)
        action.connect("activate", self.show_config_wizard)
        self.add_action(action)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(self.box)

        header = Gtk.HeaderBar()
        self.set_titlebar(header)

        # --- Main UI Components ---
        self.notebook = Gtk.Notebook()
        self.box.append(self.notebook)

        # --- Log Tab ---
        log_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        log_page.set_margin_top(6)
        log_page.set_margin_bottom(6)
        log_page.set_margin_start(6)
        log_page.set_margin_end(6)
        self.notebook.append_page(log_page, Gtk.Label(label="Log"))

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        log_page.append(scrolled_window)

        self.log_view = Gtk.TextView()
        self.log_view.set_editable(False)
        self.log_view.set_cursor_visible(False)
        self.log_buffer = self.log_view.get_buffer()
        scrolled_window.set_child(self.log_view)

        # --- Scheduler Tab ---
        scheduler_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        scheduler_page.set_margin_top(12)
        scheduler_page.set_margin_bottom(12)
        scheduler_page.set_margin_start(12)
        scheduler_page.set_margin_end(12)
        self.notebook.append_page(scheduler_page, Gtk.Label(label="Scheduler"))

        title_label = Gtk.Label()
        title_label.set_markup("<span weight='bold' size='large'>OS-Native Backup Scheduler</span>")
        title_label.set_halign(Gtk.Align.START)
        scheduler_page.append(title_label)

        desc_label = Gtk.Label(label="This scheduler uses the operating system's native task scheduler to run backups automatically, even if this application is closed.")
        desc_label.set_wrap(True)
        desc_label.set_halign(Gtk.Align.START)
        scheduler_page.append(desc_label)

        self.scheduler_status_label = Gtk.Label(label="Status: Unknown")
        self.scheduler_status_label.set_halign(Gtk.Align.START)
        self.backup_frequency_label = Gtk.Label(label="Backup Frequency: Unknown")
        self.backup_frequency_label.set_halign(Gtk.Align.START)
        
        status_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        status_box.append(self.scheduler_status_label)
        status_box.append(self.backup_frequency_label)
        scheduler_page.append(status_box)

        self.scheduler_toggle_button = Gtk.Button(label="Enable Scheduled Backup")
        self.scheduler_toggle_button.connect('clicked', self.on_toggle_schedule_clicked)
        scheduler_page.append(self.scheduler_toggle_button)

        # --- Progress Bar and Button ---
        self.progress_bar = Gtk.ProgressBar()
        self.box.append(self.progress_bar)

        self.run_button = Gtk.Button(label="Run Manual Backup")
        self.run_button.connect('clicked', self.on_run_backup_clicked)
        self.run_button.set_sensitive(False)
        self.box.append(self.run_button)

        # --- Connect Logging ---
        self.log_handler = GtkLogHandler(self.log_buffer)
        log.addHandler(self.log_handler)

        # --- Initialize Scheduler ---
        self.scheduler = get_scheduler()
        self.update_scheduler_status()

        log.info("Welcome to NotionSafe (GTK).")

    def show_config_wizard(self, action, param):
        wizard = GtkConfigWizard(transient_for=self, modal=True)
        wizard.present()
        wizard.connect("close", self.on_wizard_closed)

    def on_wizard_closed(self, wizard):
        self.update_scheduler_status()

    def on_run_backup_clicked(self, widget):
        log.info("Starting manual backup process...")
        self.run_button.set_sensitive(False)
        self.progress_bar.set_fraction(0.0)
        
        config_path = os.path.expanduser("~/.noteback/config.yaml")

        callbacks = {
            'progress': self.on_backup_progress,
            'finished': self.on_backup_finished,
            'error': self.on_backup_error,
            'invalid_token': self.on_invalid_token
        }
        
        self.worker = Worker(config_path, callbacks)
        self.worker.start()

    def on_backup_progress(self, progress):
        GLib.idle_add(self.progress_bar.set_fraction, progress / 100.0)

    def on_backup_finished(self):
        def finished_ui():
            self.progress_bar.set_fraction(1.0)
            self.run_button.set_sensitive(True)
            log.info("Backup process completed successfully.")
        GLib.idle_add(finished_ui)

    def on_backup_error(self, error_message):
        def error_ui():
            self.run_button.set_sensitive(True)
            log.error(f"An unexpected error occurred: {error_message}", exc_info=True)
            dialog = Gtk.MessageDialog(
                transient_for=self,
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Backup Failed",
                secondary_text=str(error_message)
            )
            dialog.connect("response", lambda d, r: d.destroy())
            dialog.present()
        GLib.idle_add(error_ui)

    def on_invalid_token(self):
        def invalid_token_ui():
            self.run_button.set_sensitive(True)
            log.error("Backup failed due to an invalid Notion token.")
            dialog = Gtk.MessageDialog(
                transient_for=self,
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Invalid Notion Token",
                secondary_text="The Notion API token is invalid or unauthorized. Please re-run the configuration wizard."
            )
            dialog.connect("response", lambda d, r: d.destroy())
            dialog.present()
            self.show_config_wizard(None, None)
        GLib.idle_add(invalid_token_ui)

    def update_scheduler_status(self):
        is_scheduled = self.scheduler.is_scheduled()
        if is_scheduled:
            self.scheduler_status_label.set_markup("Status: <span color='green'><b>Enabled</b></span>")
            self.scheduler_toggle_button.set_label("Disable Scheduled Backup")
        else:
            self.scheduler_status_label.set_markup("Status: <span color='red'><b>Disabled</b></span>")
            self.scheduler_toggle_button.set_label("Enable Scheduled Backup")

        config_path = os.path.expanduser("~/.noteback/config.yaml")
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            interval_hours = config['storage'].get('backup_frequency_hours', 24)
            self.backup_frequency_label.set_text(f"Backup Frequency: Every {interval_hours} hours")
        except (FileNotFoundError, KeyError):
            self.backup_frequency_label.set_text("Backup Frequency: Unknown")

    def on_toggle_schedule_clicked(self, widget):
        action = "delete-task" if "Disable" in self.scheduler_toggle_button.get_label() else "create-task"
        
        if action == "delete-task":
            success, message = self.scheduler.delete()
        else:
            config_path = os.path.expanduser("~/.noteback/config.yaml")
            try:
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                interval_hours = config['storage'].get('backup_frequency_hours', 24)
            except (FileNotFoundError, KeyError):
                log.warning("Could not read backup frequency from config. Defaulting to 24 hours.")
                interval_hours = 24
            success, message = self.scheduler.create(interval_hours)

        dialog_type = Gtk.MessageType.INFO if success else Gtk.MessageType.ERROR
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=dialog_type,
            buttons=Gtk.ButtonsType.OK,
            text="Task Scheduler",
            secondary_text=message
        )
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.present()
        
        self.update_scheduler_status()


def validate_config(config):
    """
    Validates if the essential keys are present in the config.
    Returns True if valid, False otherwise.
    """
    if not config:
        return False
    if 'storage' not in config:
        return False
    if 'local_path' not in config['storage'] or not config['storage']['local_path']:
        return False
    # A basic check for notion keys. A more thorough check could validate the token itself.
    if 'notion' not in config:
        return False
    return True

class GtkApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.win = None
        # Force dark theme
        style_manager = Adw.StyleManager.get_default()
        style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)

    def do_activate(self):
        # Create the menu model
        menu = Gio.Menu.new()
        edit_menu = Gio.Menu.new()
        edit_menu.append("Configuration", "win.show_config_wizard")
        menu.append_submenu("Edit", edit_menu)
        self.set_menubar(menu)

        config_path = os.path.expanduser("~/.noteback/config.yaml")
        config = None
        needs_config = True

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                if validate_config(config):
                    needs_config = False
            except (yaml.YAMLError, IOError) as e:
                log.error(f"Error loading or parsing config file: {e}")
                needs_config = True

        if needs_config:
            # In GTK, the main window must exist for a transient dialog.
            # We show the main window, then immediately present the wizard.
            self.show_main_window()
            # A short delay can help ensure the main window is fully drawn.
            GLib.idle_add(self.win.show_config_wizard, None, None)
        else:
            self.show_main_window()

    def show_main_window(self):
        self.win = MainWindow(application=self)
        self.win.present()

def main():
    """Main entry point for the GTK application."""
    app = GtkApp(application_id="com.example.NotionSafe")
    app.run(sys.argv)

if __name__ == '__main__':
    main()
