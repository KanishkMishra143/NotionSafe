import notion_client

class NotionAPI:
    def __init__(self, token):
        self.client = notion_client.Client(auth=token)

    def get_page(self, page_id):
        """Retrieves a Notion page."""
        return self.client.pages.retrieve(page_id=page_id)

    def get_database(self, database_id):
        """Retrieves a Notion database."""
        return self.client.databases.query(database_id=database_id)

    def get_block_children(self, block_id):
        """Retrieves the children of a block."""
        return self.client.blocks.children.list(block_id=block_id)
