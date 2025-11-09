import pytest
from unittest.mock import patch
from notebackup.auth import get_notion_token, SERVICE_ID

@patch('os.getenv')
def test_get_notion_token_from_env(mock_getenv):
    """
    Test that the token is correctly retrieved from an environment variable.
    """
    mock_getenv.return_value = "env_token"
    token = get_notion_token()
    assert token == "env_token"
    mock_getenv.assert_called_once_with("NOTION_TOKEN")

@patch('os.getenv', return_value=None)
@patch('keyring.get_password')
def test_get_notion_token_from_keyring(mock_get_password, mock_getenv):
    """
    Test that the token is correctly retrieved from the keyring.
    """
    mock_get_password.return_value = "keyring_token"
    token = get_notion_token()
    assert token == "keyring_token"
    mock_get_password.assert_called_once_with(SERVICE_ID, "notion_token")

@patch('os.getenv', return_value=None)
@patch('keyring.get_password', return_value=None)
@patch('builtins.input', side_effect=["input_token", "y"])
@patch('keyring.set_password')
def test_get_notion_token_from_input_and_save(mock_set_password, mock_input, mock_get_password, mock_getenv):
    """
    Test that the token is retrieved from user input and saved to the keyring.
    """
    token = get_notion_token()
    assert token == "input_token"
    mock_set_password.assert_called_once_with(SERVICE_ID, "notion_token", "input_token")

@patch('os.getenv', return_value=None)
@patch('keyring.get_password', return_value=None)
@patch('builtins.input', side_effect=["input_token", "n"])
@patch('keyring.set_password')
def test_get_notion_token_from_input_and_dont_save(mock_set_password, mock_input, mock_get_password, mock_getenv):
    """
    Test that the token is retrieved from user input but not saved to the keyring.
    """
    token = get_notion_token()
    assert token == "input_token"
    mock_set_password.assert_not_called()
