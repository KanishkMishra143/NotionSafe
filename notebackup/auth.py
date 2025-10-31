import os
import keyring
from dotenv import load_dotenv

SERVICE_ID = "notionsafe"

def get_notion_token():
    """
    Retrieves the Notion API token.
    It checks for an environment variable first, then the system keyring.
    If not found, it prompts the user to enter and save it to the keyring.
    """
    load_dotenv()
    token = os.getenv("NOTION_TOKEN")
    if token:
        print("Loaded Notion token from environment variable.")
        return token

    token = keyring.get_password(SERVICE_ID, "notion_token")
    if token:
        print("Loaded Notion token from keyring.")
        return token

    print("Notion token not found.")
    token = input("Please enter your Notion API token: ").strip()
    if token:
        save = input("Do you want to save this token to the system keyring? (y/n): ").lower()
        if save == 'y':
            keyring.set_password(SERVICE_ID, "notion_token", token)
            print("Token saved to keyring.")
    return token
