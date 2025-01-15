import hashlib
import json

import pytest

from server_config import ServerConfig
from storage.FileBasedKeyValueStore import FileBasedKeyValueStore


class TestFileBasedKeyValueStore:
    user = {
        "user_id": "1",
        "password_hash": hashlib.sha256("password".encode()).hexdigest()
    }

    # Initialize store with default filename and verify empty store creation
    def test_init_creates_empty_store(self, mocker):
        # Mock file operations
        mock_open = mocker.patch('builtins.open', mocker.mock_open())
        mock_json_load = mocker.patch('json.load')
        mock_json_load.side_effect = FileNotFoundError()

        # Initialize store with default filename
        store = FileBasedKeyValueStore()

        # Verify store is initialized as empty dict
        assert store.store == {}
        # Verify correct filename is set
        assert store.filename == ServerConfig.STORAGE_PATH + 'data_store.json'

    # Load from corrupted JSON file should initialize empty store
    def test_load_corrupted_json_creates_empty_store(self, mocker):
        # Mock file operations
        mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data='invalid json'))
        mock_json_load = mocker.patch('json.load')
        mock_json_load.side_effect = json.JSONDecodeError('Invalid JSON', '', 0)

        # Initialize store which triggers load
        store = FileBasedKeyValueStore()

        # Verify store is initialized as empty dict
        assert store.store == {}

    # Set new key-value pair and verify successful storage
    def test_set_new_key_value_pair(self, mocker):
        # Mock file operations
        mock_open = mocker.patch('builtins.open', mocker.mock_open())
        mock_json_dump = mocker.patch('json.dump')

        # Initialize store with default filename
        store = FileBasedKeyValueStore()

        # Set a new key-value pair
        key = 'test_key'
        value = ['value1', 'value2']
        store.set(key, value)

        # Verify the key-value pair is stored correctly
        assert store.store[key] == value

        # Verify that the data was saved to the file
        mock_json_dump.assert_called_once_with(store.store, mock_open())

    # Add value to existing key's list and verify append
    def test_add_value_to_existing_key(self, mocker):
        # Mock file operations
        mock_open = mocker.patch('builtins.open', mocker.mock_open())
        mock_json_load = mocker.patch('json.load')
        mock_json_load.return_value = {'key1': ['initial_value']}
        mock_json_dump = mocker.patch('json.dump')

        # Initialize store with default filename
        store = FileBasedKeyValueStore()

        # Add a new value to the existing key's list
        store.add('key1', 'new_value')

        # Verify the value is appended to the list
        assert store.store['key1'] == ['initial_value', 'new_value']

        # Verify that the data was saved with the new value appended
        mock_json_dump.assert_called_once_with({'key1': ['initial_value', 'new_value']}, mock_open())

    # Verify key-value pair is stored in memory
    def test_set_stores_key_value_pair(self, mocker):
        # Mock file operations
        mock_open = mocker.patch('builtins.open', mocker.mock_open())
        mock_json_load = mocker.patch('json.load')
        mock_json_load.side_effect = FileNotFoundError()
        mock_json_dump = mocker.patch('json.dump')

        # Initialize store with default filename
        store = FileBasedKeyValueStore()

        # Set a key-value pair
        key = 'test_key'
        value = ['test_value']
        store.set(key, value)

        # Verify the key-value pair is stored in memory
        assert store.store[key] == value

        # Verify that the data was saved to the file
        mock_json_dump.assert_called_once_with(store.store, mock_open())

    # Get existing key returns correct value list
    def test_get_existing_key_returns_correct_value_list(self):
        store = FileBasedKeyValueStore()

        # Get the value for an existing key
        result = store.get("key1")

        # Verify the correct value list is returned
        assert result == ["value1", "value2"]

    # Verify new value is appended to existing list
    def test_add_appends_value_to_existing_list(self, mocker):
        # Mock file operations
        mock_open = mocker.patch('builtins.open', mocker.mock_open())
        mock_json_load = mocker.patch('json.load')
        mock_json_dump = mocker.patch('json.dump')

        # Set up initial store data
        initial_data = {'key1': ['value1']}
        mock_json_load.return_value = initial_data

        # Initialize store
        store = FileBasedKeyValueStore()

        # Add new value to existing key's list
        store.add('key1', 'value2')

        # Verify the new value is appended
        assert store.store['key1'] == ['value1', 'value2']

        # Verify data is saved with the new value appended
        mock_json_dump.assert_called_once_with({'key1': ['value1', 'value2']}, mock_open())

    # Verify returned list matches stored list
    def test_get_existing_key_returns_correct_value_list(self, mocker):
        # Mock file operations
        mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data='{"key1": ["value1", "value2"]}'))
        mock_json_load = mocker.patch('json.load', return_value={"key1": ["value1", "value2"]})

        # Initialize store with default filename
        store = FileBasedKeyValueStore()

        # Verify the returned list matches the stored list
        assert store.get("key1") == ["value1", "value2"]

    # Confirm get operation doesn't modify stored data
    def test_get_operation_does_not_modify_data(self, mocker):
        # Mock file operations
        mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data='{"key1": [1, 2, 3]}'))
        mock_json_load = mocker.patch('json.load', return_value={"key1": [1, 2, 3]})

        # Initialize store with default filename
        store = FileBasedKeyValueStore()

        # Perform get operation
        result = store.get("key1")

        # Verify the returned value is correct
        assert result == [1, 2, 3]

        # Verify the store data remains unchanged
        assert store.store == {"key1": [1, 2, 3]}

    # Delete existing key and verify removal
    def test_delete_existing_key(self, mocker):
        # Mock file operations
        mock_open = mocker.patch('builtins.open', mocker.mock_open())
        mock_json_load = mocker.patch('json.load')
        mock_json_dump = mocker.patch('json.dump')

        # Set up initial store data
        initial_data = {'key1': [1, 2, 3]}
        mock_json_load.return_value = initial_data

        # Initialize store
        store = FileBasedKeyValueStore()

        # Verify initial data is loaded
        assert store.store == initial_data

        # Delete existing key
        store.delete('key1')

        # Verify key is removed
        assert 'key1' not in store.store

        # Verify data is saved after deletion
        mock_json_dump.assert_called_once_with({}, mock_open())

    # Create store with custom filename and verify data persistence
    def test_custom_filename_persistence(self, mocker):
        # Mock file operations
        mock_open = mocker.patch('builtins.open', mocker.mock_open())
        mock_json_load = mocker.patch('json.load')
        mock_json_dump = mocker.patch('json.dump')
        mock_json_load.side_effect = FileNotFoundError()

        # Initialize store with custom filename
        custom_filename = 'custom_store.json'
        store = FileBasedKeyValueStore(filename=custom_filename)

        # Verify store is initialized as empty dict
        assert store.store == {}
        # Verify correct custom filename is set
        assert store.filename == ServerConfig.STORAGE_PATH + custom_filename

        # Set a key-value pair and verify persistence
        store.set('key1', ['value1'])
        mock_open.assert_called_with(ServerConfig.STORAGE_PATH + custom_filename, 'w')
        mock_json_dump.assert_called_with({'key1': ['value1']}, mock_open())

    # Set value with non-list type raises ValueError
    def test_set_raises_value_error_for_non_list_value(self, mocker):
        # Mock file operations
        mock_open = mocker.patch('builtins.open', mocker.mock_open())
        mock_json_load = mocker.patch('json.load')
        mock_json_load.side_effect = FileNotFoundError()

        # Initialize store with default filename
        store = FileBasedKeyValueStore()

        # Attempt to set a non-list value and expect ValueError
        with pytest.raises(ValueError, match="The value for key '123' must be a list."):
            store.set('key1', 123)
