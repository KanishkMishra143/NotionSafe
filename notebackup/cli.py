import argparse
import os
import yaml
import notion_client
from notion_client.errors import APIResponseError
from . import auth, exporter, fs_layout, storage, gitops
from .logger import log
from .post_process import post_process_file

class InvalidNotionTokenError(Exception):
    """Custom exception for invalid Notion API tokens."""
    pass

def get_page_title(notion, page_id):
    try:
        page = notion.pages.retrieve(page_id)
        return page['properties']['title']['title'][0]['plain_text']
    except Exception as e:
        log.error(f"Failed to get title for page {page_id}: {e}")
        return page_id

def load_config(config_path):
    config_path = os.path.expanduser(config_path)
    if not os.path.exists(config_path):
        log.error(f"Configuration file not found at {config_path}")
        return None
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def run_backup(config, progress_callback=None):
    token = auth.get_notion_token()
    if not token:
        log.error("Failed to get Notion token. Exiting.")
        return False

    try:
        notion = notion_client.Client(auth=token)
        # Test the token by making a simple API call (e.g., list users or search)
        # This helps catch invalid tokens early before expensive export operations.
        # A simple request like a user list often works.
        notion.users.list()
    except APIResponseError as e:
        if e.code == 'unauthorized' or 'unauthorized' in str(e).lower() or '401' in str(e):
            raise InvalidNotionTokenError("The provided Notion API token is invalid or unauthorized.") from e
        else:
            raise # Re-raise other API errors
    except Exception as e:
        log.error(f"An unexpected error occurred during Notion client initialization or token validation: {e}", exc_info=True)
        return False

    local_backup_path = os.path.normpath(os.path.expanduser(config['storage']['local_path']))
    snapshot_path = fs_layout.create_snapshot_dir(local_backup_path)
    log.info(f"Created snapshot directory: {snapshot_path}")

    page_ids = config['notion'].get('page_ids', [])
    db_ids = config['notion'].get('database_ids', [])
    total_items = len(page_ids) + len(db_ids)
    processed_items = 0
    has_errors = False

    base_args = ['--token', token, '--path', snapshot_path, '--unzipped']

    for page_id in page_ids:
        page_title = get_page_title(notion, page_id)
        log.info(f"Exporting page: {page_title}")
        try:
            result = exporter.export_cli(base_args + ['--id', page_id, '--name', page_title])
            if result != 0:
                raise Exception(f"Exporter failed for page {page_id} with exit code {result}")
            post_process_file(os.path.join(snapshot_path, f"{page_title}.md"))
        except Exception as e:
            log.error(f"Failed to export page {page_id}: {e}", exc_info=True)
            has_errors = True
        finally:
            processed_items += 1
            if progress_callback:
                progress = int((processed_items / total_items) * 100)
                progress_callback(progress)

    for db_id in db_ids:
        log.info(f"Exporting database: {db_id}")
        try:
            result = exporter.export_cli(base_args + ['--id', db_id, '--name', db_id])
            if result != 0:
                raise Exception(f"Exporter failed for database {db_id} with exit code {result}")
            post_process_file(os.path.join(snapshot_path, f"{db_id}.md"))
        except Exception as e:
            log.error(f"Failed to export database {db_id}: {e}", exc_info=True)
            has_errors = True
        finally:
            processed_items += 1
            if progress_callback:
                progress = int((processed_items / total_items) * 100)
                progress_callback(progress)

    if has_errors:
        log.error("Backup process completed with errors.")
        return False

    fs_layout.update_latest_marker(local_backup_path, snapshot_path)

    if config['storage']['external_drive']['enabled']:
        ext_path = os.path.expanduser(config['storage']['external_drive']['path'])
        storage.rsync_to_external(snapshot_path, ext_path)

    if config['storage']['git']['enabled']:
        git_config = config['storage']['git']
        gitops.perform_git_backup(
            repo_path=local_backup_path, 
            snapshot_folder=snapshot_path,
            remote_name=git_config['remote_name'], 
            remote_url=git_config['remote_url']
        )

    log.info("Backup process completed successfully!")
    return True

def main(config_path='~/.noteback/config.yaml', progress_callback=None):
    config = load_config(config_path)
    if config:
        return run_backup(config, progress_callback)
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="NotionSafe: Backup your Notion workspace.")
    parser.add_argument('--config', default='~/.noteback/config.yaml', help='Path to the configuration file.')
    args = parser.parse_args()
    if not main(config_path=args.config):
        sys.exit(1)
