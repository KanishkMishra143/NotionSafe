import notion_client
from notebackup import auth

def preprocess_page(page_id):
    token = auth.get_notion_token()
    notion = notion_client.Client(auth=token)

    blocks = notion.blocks.children.list(block_id=page_id)["results"]

    for block in blocks:
        if block["type"] == "callout":
            # Remove the icon from the callout block
            if "icon" in block["callout"]:
                del block["callout"]["icon"]

    return blocks

if __name__ == '__main__':
    page_id = "1b80a912-02c3-8002-901c-e4285698b0cc"
    modified_blocks = preprocess_page(page_id)
    print(modified_blocks)
