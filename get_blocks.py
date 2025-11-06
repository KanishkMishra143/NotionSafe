import notion_client
from notebackup import auth

page_id = "1b80a912-02c3-8002-901c-e4285698b0cc"
token = auth.get_notion_token()

notion = notion_client.Client(auth=token)

blocks = notion.blocks.children.list(block_id=page_id)

print(blocks)
