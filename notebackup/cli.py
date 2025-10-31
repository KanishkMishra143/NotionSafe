import argparse
import os
import yaml
from . import auth, exporter, fs_layout, storage, scheduler

def main():
    parser = argparse.ArgumentParser(description="NotionSafe: Backup your Notion workspace.")
    parser.add_argument('--config', default='~/.noteback/config.yaml', help='Path to the configuration file.')
    parser.add_argument('--install-timer', action='store_true', help='Install and enable a systemd user timer.')
    parser.add_argument('--cron-job', action='store_true', help='Show instructions for setting up a cron job.')

    args = parser.parse_args()

    if args.install_timer:
        scheduler.install_systemd_timer()
        return
    
    if args.cron_job:
        scheduler.add_cron_job()
        return

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

    local_backup_path = os.path.expanduser(config['storage']['local_path'])
    snapshot_path = fs_layout.create_snapshot_dir(local_backup_path)
    print(f"Created snapshot directory: {snapshot_path}")

    page_ids = config['notion'].get('page_ids', [])
    db_ids = config['notion'].get('database_ids', [])

    if page_ids:
        exporter.export_pages(page_ids, snapshot_path)
    if db_ids:
        exporter.export_databases(db_ids, snapshot_path)

    fs_layout.update_latest_symlink(local_backup_path, snapshot_path)

    if config['storage']['external_drive']['enabled']:
        ext_path = os.path.expanduser(config['storage']['external_drive']['path'])
        storage.rsync_to_external(snapshot_path, ext_path)

    if config['storage']['git']['enabled']:
        git_config = config['storage']['git']
        storage.git_commit(local_backup_path, os.path.basename(snapshot_path), git_config['remote_name'], git_config['remote_url'])

    print("\nBackup process completed successfully!")

if __name__ == '__main__':
    main()
