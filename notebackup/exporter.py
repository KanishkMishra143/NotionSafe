from notion2md.exporter import export_cli
import os

def export_pages(page_ids, output_path):
    """
    Exports Notion pages to Markdown using notion2md.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for page_id in page_ids:
        try:
            print(f"Exporting page: {page_id}")
            # notion2md CLI arguments: --id, --type, --output
            export_cli(id=page_id, type="page", output_path=output_path, download=True)
            print(f"Successfully exported page: {page_id}")
        except Exception as e:
            print(f"Error exporting page {page_id}: {e}")

def export_databases(database_ids, output_path):
    """
    Exports Notion databases to Markdown using notion2md.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for db_id in database_ids:
        try:
            print(f"Exporting database: {db_id}")
            export_cli(id=db_id, type="database", output_path=output_path, download=True)
            print(f"Successfully exported database: {db_id}")
        except Exception as e:
            print(f"Error exporting database {db_id}: {e}")
