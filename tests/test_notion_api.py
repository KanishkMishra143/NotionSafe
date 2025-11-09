import pytest
from unittest.mock import patch, MagicMock
from notebackup.notion_api import NotionAPI

@patch('notion_client.Client')
def test_notion_api_init(mock_client):
    """
    Test that the NotionAPI class initializes the notion_client.Client correctly.
    """
    api = NotionAPI("test_token")
    mock_client.assert_called_once_with(auth="test_token")

@patch('notion_client.Client')
def test_get_page(mock_client):
    """
    Test that get_page calls the correct method on the notion_client.
    """
    mock_pages = MagicMock()
    mock_client.return_value.pages = mock_pages

    api = NotionAPI("test_token")
    api.get_page("test_page_id")

    mock_pages.retrieve.assert_called_once_with(page_id="test_page_id")

@patch('notion_client.Client')
def test_get_database(mock_client):
    """
    Test that get_database calls the correct method on the notion_client.
    """
    mock_databases = MagicMock()
    mock_client.return_value.databases = mock_databases

    api = NotionAPI("test_token")
    api.get_database("test_db_id")

    mock_databases.query.assert_called_once_with(database_id="test_db_id")

@patch('notion_client.Client')
def test_get_block_children(mock_client):
    """
    Test that get_block_children calls the correct method on the notion_client.
    """
    mock_blocks = MagicMock()
    mock_client.return_value.blocks = mock_blocks

    api = NotionAPI("test_token")
    api.get_block_children("test_block_id")

    mock_blocks.children.list.assert_called_once_with(block_id="test_block_id")
