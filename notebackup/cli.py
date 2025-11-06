import argparse
import os
import yaml
import notion_client
from . import auth, exporter, fs_layout, storage, scheduler, gitops
from post_process import post_process_file

def get_page_title(notion, page_id):
    try:
        page = notion.pages.retrieve(page_id)
        # The title is a rich text object, so we need to extract the plain text
        return page['properties']['title']['title'][0]['plain_text']
    except Exception as e:
        print(f"    ERROR: Failed to get title for page {page_id}: {e}")
        return page_id

def main():
    parser = argparse.ArgumentParser(description="NotionSafe: Backup your Notion workspace.")
    parser.add_argument('--config', default='~/.noteback/config.yaml', help='Path to the configuration file.')

    args = parser.parse_args()

    config_path = os.path.expanduser(args.config)
    if not os.path.exists(config_path):
        print(f"Configuration file not found at {config_path}")
        # As a fallback, try to use the example config
        example_config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'examples', 'backup_config.yaml'))
        if os.path.exists(example_config_path):
            print(f"Using example configuration file: {example_config_path}")
            config_path = example_config_path
        else:
            return

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    token = auth.get_notion_token()
    if not token:
        print("Failed to get Notion token. Exiting.")
        return

    notion = notion_client.Client(auth=token)

    local_backup_path = os.path.expanduser(config['storage']['local_path'])
    snapshot_path = fs_layout.create_snapshot_dir(local_backup_path)
    print(f"Created snapshot directory: {snapshot_path}")

    page_ids = config['notion'].get('page_ids', [])
    db_ids = config['notion'].get('database_ids', [])

    # The exporter expects a list of arguments for the notion2md CLI
    base_args = ['--token', token, '--path', snapshot_path, '--unzipped']

    for page_id in page_ids:
        page_title = get_page_title(notion, page_id)
        print(f"Exporting page: {page_title}")
        try:
            exporter.export_cli(base_args + ['--id', page_id, '--name', page_title])
            post_process_file(os.path.join(snapshot_path, f"{page_title}.md"))
        except Exception as e:
            print(f"    ERROR: Failed to export page {page_id}: {e}")

    for db_id in db_ids:
        # For databases, we'll use the database ID as the name for now
        print(f"Exporting database: {db_id}")
        try:
            exporter.export_cli(base_args + ['--id', db_id, '--name', db_id])
            post_process_file(os.path.join(snapshot_path, f"{db_id}.md"))
        except Exception as e:
            print(f"    ERROR: Failed to export database {db_id}: {e}")

    fs_layout.update_latest_marker(local_backup_path, snapshot_path)

    if config['storage']['external_drive']['enabled']:
        ext_path = os.path.expanduser(config['storage']['external_drive']['path'])
        storage.rsync_to_external(snapshot_path, ext_path)

    if config['storage']['git']['enabled']:
        git_config = config['storage']['git']
        # The repo path is the local backup path where the .git folder resides
        gitops.perform_git_backup(
            repo_path=local_backup_path, 
            snapshot_folder=snapshot_path, # Pass the full path to the snapshot
            remote_name=git_config['remote_name'], 
            remote_url=git_config['remote_url']
        )

    print("\nBackup process completed successfully!")

if __name__ == '__main__':
    main()