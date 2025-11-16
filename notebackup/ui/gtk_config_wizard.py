# notebackup/ui/gtk_config_wizard.py

import sys
import os
import yaml
import gi
import keyring
import threading
import notion_client

from ..auth import SERVICE_ID
from ..logger import log

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio, GObject, GLib

class ListItem(GObject.Object):
    __gtype_name__ = 'ListItem'
    
    title = GObject.Property(type=str)
    item_id = GObject.Property(type=str)
    checked = GObject.Property(type=bool, default=False)

    def __init__(self, title, item_id):
        super().__init__()
        self.title = title
        self.item_id = item_id

class SchedulePage(Gtk.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_spacing(12)
        self.set_margin_top(12)
        self.set_margin_bottom(12)
        self.set_margin_start(12)
        self.set_margin_end(12)

        self.schedule_check = Gtk.CheckButton(label="Enable automatic backups")
        self.append(self.schedule_check)

        self.frequency_dropdown = Gtk.DropDown.new_from_strings([
            "Every 12 hours", "Every 24 hours", "Every 48 hours"
        ])
        self.frequency_dropdown.set_selected(1) # Default to 24 hours
        self.frequency_dropdown.set_sensitive(False)
        self.append(self.frequency_dropdown)

        self.schedule_check.connect('toggled', lambda cb: self.frequency_dropdown.set_sensitive(cb.get_active()))

    def get_schedule_data(self):
        if not self.schedule_check.get_active():
            return None
        
        selected_text = self.frequency_dropdown.get_selected_item().get_string()
        hours = int(selected_text.split()[1])
        return hours

class NotionContentPage(Gtk.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_spacing(6)
        self.set_margin_top(12)
        self.set_margin_bottom(12)
        self.set_margin_start(12)
        self.set_margin_end(12)

        self.fetch_button = Gtk.Button(label="Fetch Pages & Databases")
        self.fetch_button.connect('clicked', self.on_fetch_clicked)
        self.append(self.fetch_button)

        self.append(Gtk.Label(label="Pages:", halign=Gtk.Align.START))
        self.page_list_store = Gio.ListStore(item_type=ListItem)
        self.page_list_view = self.create_list_view(self.page_list_store)
        self.append(self.page_list_view)

        self.append(Gtk.Label(label="Databases:", halign=Gtk.Align.START))
        self.db_list_store = Gio.ListStore(item_type=ListItem)
        self.db_list_view = self.create_list_view(self.db_list_store)
        self.append(self.db_list_view)

    def create_list_view(self, store):
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_factory_setup)
        factory.connect("bind", self._on_factory_bind)

        selection_model = Gtk.NoSelection(model=store)
        list_view = Gtk.ListView(model=selection_model, factory=factory)
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_child(list_view)
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_min_content_height(150)
        return scrolled_window

    def _on_factory_setup(self, factory, list_item):
        box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.HORIZONTAL)
        check = Gtk.CheckButton()
        label = Gtk.Label()
        box.append(check)
        box.append(label)
        list_item.set_child(box)

    def _on_factory_bind(self, factory, list_item):
        box = list_item.get_child()
        check_button = box.get_first_child()
        label = box.get_last_child()
        
        item = list_item.get_item()
        label.set_label(item.title)
        check_button.set_active(item.checked)
        
        check_button.connect('toggled', self._on_item_toggled, item)

    def _on_item_toggled(self, check_button, item):
        item.checked = check_button.get_active()

    def on_fetch_clicked(self, button):
        wizard = self.get_ancestor(Gtk.Assistant)
        token = wizard.api_page.get_token() if wizard else None
        
        if not token:
            dialog = Gtk.MessageDialog(
                transient_for=self.get_root(), modal=True,
                message_type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,
                text="Missing Token", secondary_text="Please enter a Notion API token on the previous page."
            )
            dialog.connect("response", lambda d, r: d.destroy())
            dialog.present()
            return

        self.fetch_button.set_sensitive(False)
        self.fetch_button.set_label("Fetching...")
        
        thread = threading.Thread(target=self.fetch_thread_func, args=(token,))
        thread.start()

    def fetch_thread_func(self, token):
        try:
            notion = notion_client.Client(auth=token)
            results = notion.search()["results"]
            GLib.idle_add(self.on_fetch_success, results)
        except Exception as e:
            GLib.idle_add(self.on_fetch_error, e)

    def on_fetch_success(self, results):
        self.page_list_store.remove_all()
        self.db_list_store.remove_all()

        for result in results:
            item_id = result.get("id")
            if result["object"] == "page":
                title_list = result.get("properties", {}).get("title", {}).get("title", [])
                title = title_list[0].get("plain_text", item_id) if title_list else item_id
                self.page_list_store.append(ListItem(title, item_id))
            elif result["object"] == "database":
                title_list = result.get("title", [])
                title = title_list[0].get("plain_text", item_id) if title_list else item_id
                self.db_list_store.append(ListItem(title, item_id))
        
        log.info(f"Successfully fetched {self.page_list_store.get_n_items()} pages and {self.db_list_store.get_n_items()} databases.")
        self.fetch_button.set_sensitive(True)
        self.fetch_button.set_label("Fetch Pages & Databases")

    def on_fetch_error(self, error):
        log.error(f"Failed to fetch from Notion: {error}", exc_info=True)
        dialog = Gtk.MessageDialog(
            transient_for=self.get_root(), modal=True,
            message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK,
            text="API Error", secondary_text=f"Failed to fetch from Notion: {error}"
        )
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.present()
        self.fetch_button.set_sensitive(True)
        self.fetch_button.set_label("Fetch Pages & Databases")

    def get_selected_page_ids(self):
        return self.get_selected_ids(self.page_list_store)

    def get_selected_db_ids(self):
        return self.get_selected_ids(self.db_list_store)

    def get_selected_ids(self, store):
        selected_ids = []
        for i in range(store.get_n_items()):
            item = store.get_item(i)
            if item.checked:
                selected_ids.append(item.item_id)
        return selected_ids

class NotionApiPage(Gtk.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_spacing(12)
        self.set_margin_top(12)
        self.set_margin_bottom(12)
        self.set_margin_start(12)
        self.set_margin_end(12)

        self.append(Gtk.Label(label="Enter your Notion Integration Token:", halign=Gtk.Align.START))
        
        self.token_edit = Gtk.Entry(visibility=False, placeholder_text="secret_...")
        self.append(self.token_edit)

    def prepare(self):
        existing_token = keyring.get_password(SERVICE_ID, "notion_token")
        if existing_token:
            self.token_edit.set_text(existing_token)

    def get_token(self):
        return self.token_edit.get_text()

class StoragePage(Gtk.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_spacing(12)
        self.set_margin_top(12)
        self.set_margin_bottom(12)
        self.set_margin_start(12)
        self.set_margin_end(12)

        # --- Local Backup ---
        self.local_check = Gtk.CheckButton(label="Enable Local Backup")
        self.local_check.set_active(True)
        self.append(self.local_check)

        self.local_path_edit = Gtk.Entry(placeholder_text="e.g., ~/Documents/NotionBackups")
        self.append(self.local_path_edit)

        local_browse_button = Gtk.Button(label="Browse...")
        local_browse_button.connect('clicked', self.on_browse_local_clicked)
        self.append(local_browse_button)

        # --- External Drive ---
        self.external_check = Gtk.CheckButton(label="Enable External Drive Copy")
        self.append(self.external_check)

        self.external_path_edit = Gtk.Entry(placeholder_text="e.g., /Volumes/MyUSB/NotionBackups")
        self.external_path_edit.set_sensitive(False)
        self.append(self.external_path_edit)

        external_browse_button = Gtk.Button(label="Browse...")
        external_browse_button.connect('clicked', self.on_browse_external_clicked)
        self.append(external_browse_button)

        # --- Git Backup ---
        self.git_check = Gtk.CheckButton(label="Enable Git Versioning")
        self.append(self.git_check)

        self.git_url_edit = Gtk.Entry(placeholder_text="e.g., git@github.com:user/repo.git")
        self.git_url_edit.set_sensitive(False)
        self.append(self.git_url_edit)

        # --- Connections ---
        self.external_check.connect('toggled', lambda cb: self.external_path_edit.set_sensitive(cb.get_active()))
        self.git_check.connect('toggled', lambda cb: self.git_url_edit.set_sensitive(cb.get_active()))

    def on_browse_local_clicked(self, button):
        self.browse_for_folder(self.local_path_edit)

    def on_browse_external_clicked(self, button):
        self.browse_for_folder(self.external_path_edit)

    def browse_for_folder(self, entry_widget):
        dialog = Gtk.FileChooserDialog(
            title="Select a Folder",
            transient_for=self.get_root(),
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            modal=True
        )
        dialog.add_buttons("_Cancel", Gtk.ResponseType.CANCEL, "_Open", Gtk.ResponseType.OK)
        
        def on_response(d, response_id):
            if response_id == Gtk.ResponseType.OK:
                entry_widget.set_text(d.get_file().get_path())
            d.destroy()
            
        dialog.connect("response", on_response)
        dialog.present()

    def get_storage_data(self):
        return {
            'local_path': self.local_path_edit.get_text() if self.local_check.get_active() else None,
            'external_path': self.external_path_edit.get_text() if self.external_check.get_active() else None,
            'git_url': self.git_url_edit.get_text() if self.git_check.get_active() else None,
        }

class GtkConfigWizard(Gtk.Assistant):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(600, 400)
        self.set_title("NotionSafe Configuration Wizard (GTK)")

        self.connect("apply", self.on_apply)
        self.connect("close", self.on_close)
        self.connect("cancel", self.on_close)
        self.connect("prepare", self.on_prepare)

        self.add_pages()

    def add_pages(self):
        # Welcome Page
        welcome_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append_page(welcome_box)
        self.set_page_title(welcome_box, "Welcome to NotionSafe")
        self.set_page_type(welcome_box, Gtk.AssistantPageType.INTRO)
        welcome_box.append(Gtk.Label(label="This wizard will guide you through creating your backup configuration file."))
        self.set_page_complete(welcome_box, True)

        # Storage Page
        self.storage_page = StoragePage()
        self.append_page(self.storage_page)
        self.set_page_title(self.storage_page, "Storage Options")
        self.set_page_type(self.storage_page, Gtk.AssistantPageType.CONTENT)
        self.set_page_complete(self.storage_page, True)

        # Notion API Page
        self.api_page = NotionApiPage()
        self.append_page(self.api_page)
        self.set_page_title(self.api_page, "Notion Integration")
        self.set_page_type(self.api_page, Gtk.AssistantPageType.CONTENT)

        # Notion Content Page
        self.content_page = NotionContentPage()
        self.append_page(self.content_page)
        self.set_page_title(self.content_page, "Content Selection")
        self.set_page_type(self.content_page, Gtk.AssistantPageType.CONTENT)
        self.set_page_complete(self.content_page, True)

        # Schedule Page
        self.schedule_page = SchedulePage()
        self.append_page(self.schedule_page)
        self.set_page_title(self.schedule_page, "Backup Frequency")
        self.set_page_type(self.schedule_page, Gtk.AssistantPageType.CONTENT)
        self.set_page_complete(self.schedule_page, True)

        # Summary Page
        summary_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append_page(summary_box)
        self.set_page_title(summary_box, "Configuration Complete")
        self.set_page_type(summary_box, Gtk.AssistantPageType.CONFIRM)
        summary_box.append(Gtk.Label(label="Click 'Apply' to save your configuration."))

    def on_prepare(self, widget, page):
        page_num = self.get_current_page()
        if page_num == 2: # Notion API Page
            self.api_page.prepare()

    def on_apply(self, widget):
        log.info("Applying new configuration from wizard.")
        
        # Gather data
        token = self.api_page.get_token()
        storage_data = self.storage_page.get_storage_data()
        backup_frequency = self.schedule_page.get_schedule_data()
        
        config = {
            'storage': {
                'backup_path': storage_data['local_path'],
                'external_drive': storage_data['external_path'],
                'backup_frequency_hours': backup_frequency
            },
            'notion': {
                'page_ids': self.content_page.get_selected_page_ids(),
                'database_ids': self.content_page.get_selected_db_ids()
            },
            'git': {
                'use_git': bool(storage_data['git_url']),
                'remote_url': storage_data['git_url']
            }
        }

        # Save token and config
        try:
            keyring.set_password(SERVICE_ID, "notion_token", token)
            
            config_dir = os.path.expanduser("~/.noteback")
            os.makedirs(config_dir, exist_ok=True)
            config_path = os.path.join(config_dir, "config.yaml")
            
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
            log.info(f"Configuration successfully saved to {config_path}")
            
        except Exception as e:
            log.error(f"Failed to save configuration: {e}", exc_info=True)
            dialog = Gtk.MessageDialog(
                transient_for=self.get_root(), modal=True,
                message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK,
                text="Save Failed", secondary_text=f"Could not save configuration: {e}"
            )
            dialog.connect("response", lambda d, r: d.destroy())
            dialog.present()
        
        self.destroy()

    def on_close(self, widget):
        self.destroy()

if __name__ == '__main__':
    # This is for standalone testing of the wizard
    app = Gtk.Application()
    def on_activate(app):
        win = Gtk.ApplicationWindow(application=app)
        wizard = GtkConfigWizard(transient_for=win, modal=True)
        wizard.present()
    app.connect('activate', on_activate)
    app.run(None)
