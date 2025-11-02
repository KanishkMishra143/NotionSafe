#!/usr/bin/env python3
import os
import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm
import keyring
import notion_client
import yaml
import questionary

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from notebackup.auth import SERVICE_ID


def main():
    console = Console()
    console.print(
        "[bold green]Welcome to the NotionSafe interactive configuration![/bold green]"
    )
    console.print("I will guide you through creating your config.yaml file.")

    # Prompt for storage options
    enable_local = Confirm.ask("Enable local backup?", default=True)
    local_path = ""
    if enable_local:
        local_path = Prompt.ask("Enter the local path for your backups")

    enable_external = Confirm.ask("Enable external drive backup?", default=False)
    external_path = ""
    if enable_external:
        external_path = Prompt.ask("Enter the path to your external drive")

    enable_git = Confirm.ask("Enable Git remote backup?", default=False)
    remote_url = ""
    if enable_git:
        remote_url = Prompt.ask("Enter the remote Git URL")

    # Get Notion API key
    console.print("\n[bold]Now, let's connect to your Notion account.[/bold]")
    console.print("You will need a Notion integration token.")
    console.print(
        "You can get one from [link=https://www.notion.so/my-integrations]https://www.notion.so/my-integrations[/link]"
    )
    api_key = keyring.get_password(SERVICE_ID, "notion_token")
    if not api_key:
        api_key = Prompt.ask("Enter your Notion Integration Token", password=True)
        keyring.set_password(SERVICE_ID, "notion_token", api_key)
        console.print("[green]Notion token saved to your system's keyring.[/green]")
    else:
        console.print("[green]Notion token found in your system's keyring.[/green]")

    # Fetch Pages and Database IDs from Notion
    notion = notion_client.Client(auth=api_key)
    pages = []
    databases = []

    try:
        results = notion.search()["results"]
        for result in results:
            if result["object"] == "page":
                pages.append(result)
            elif result["object"] == "database":
                databases.append(result)
    except notion_client.errors.APIResponseError as e:
        console.print(f"[bold red]Error fetching from Notion API: {e}[/bold red]")
        console.print(
            "Please make sure your API key is correct and that you have shared pages/databases with the integration."
        )
        return

    # --- User Selection ---
    console.print(
        "\\n[bold]Next, you will select the pages and databases to include in the backup.[/bold]"
    )

    selected_page_ids = []
    if pages:
        console.print("\\n--- Select Pages ---")
        page_choices = [
            {
                "name": page.get("properties", {}).get("title", {}).get("title",
                [])[0].get("text", {}).get("content", "untitled"),
                "value":page["id"]
            }
            for page in pages if page.get("properties", {}).get("title", {}).get("title", [])
        ]

        selected_pages = questionary.checkbox(
            "Select the pages you want to back up (use spacebar to select)",
            choices = [choice["name"] for choice in page_choices]
        ).ask()

        if selected_pages:
            selected_page_ids = [
                choice["value"] for choice in page_choices if choice["name"] in selected_pages
            ]

        selected_database_ids = []
        if databases:
            console.print("\\n--- Select Databases ---")
            db_choices = [
                {
                    "name": db.get("title", [])[0].get("text", {}).get("content", "untitled"),
                }
                for db in databases if db.get("title", [])
            ]

            selected_dbs = questionary.checkbox(
                "Select the databases you want to back up",
                choices = [choice["name"] for choice in db_choices]
            ).ask()

            if selected_dbs:
                selected_database_ids = [
                    choice["value"] for choice in db_choices if choice["name"] in selected_dbs
                ]

        console.print(f"\\n[green]Selection complete![/green]")
        console.print(
            f"You selected {len(selected_page_ids)} page(s) and {len(selected_database_ids)} database(s)."
        )
        # --- Create Backup Directories ---
        console.print("\\n[bold]Creating necessary backup directories...[/bold]")
        if enable_local and local_path:
            try:
                full_local_path = os.path.expanduser(local_path)
                os.makedirs(full_local_path, exist_ok=True)  
                console.print(f"[green]Created local backup directory: {full_local_path}[/green]")
            except OSError as e:
                console.print(f"[bold red]Error creating local backup directory {full_local_path}: {e}[/bold red]")
        
        if enable_external and external_path:
            try:
                full_external_path = os.path.expanduser(external_path)
                os.makedirs(full_external_path, exist_ok=True)
                console.print(f"[green]Created external backup directory: {full_external_path}[/green]")
            except OSError as e:
                console.print(f"[bold red]Error creating external backup directory {full_external_path}: {e}[/bold red]") 
        
    # Generate config.yaml
    console.print("\\n[bold]Generating config.yaml file...[/bold]")

    config_data = {
        "notion": {
            "page_ids": selected_page_ids,
            "database_ids": selected_database_ids,
        },
        "storage": {
            "local": {"enabled": enable_local, "path": os.path.expanduser(local_path) if enable_local else ""}
        },
        "external_drive": {
            "enabled": enable_external,
            "path": os.path.expanduser(external_path) if enable_external else "",
        },
        "git_remote": {
            "enabled": enable_git,
            "remote_url": remote_url if enable_git else ""
        },
    }

    config_dir = os.path.expanduser("~/.noteback")
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "config.yaml")

    try:
        with open(config_path, "w") as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)
        console.print(f"[green]Successfully created config file at: {config_path}[/green]")
    except IOError as e:
        console.print(f"[bold red]Error writing config file: {e}[/bold red]")
                
if __name__ == "__main__":
    main()
