import pytest

from Models.User import UserModel, convert_user_model_to_user
from server import get_value, GetValueRequestBody, buffer_store
from storage.FileBasedKeyValueStore import FileBasedKeyValueStore
from tests.start_test import test_user


class TestGetValue:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Clear the buffer and storage before each test."""
        buffer_store.clear()
        store = FileBasedKeyValueStore(convert_user_model_to_user(test_user).get_user_filename())
        store.store.clear()
        store._save_data()

    # Return correct value for existing key in store
    def test_get_value_returns_correct_value(self, mocker):
        # Arrange
        test_key = "test_key"
        test_value = ["test_value"]

        mock_store = mocker.Mock()
        mock_store.get.return_value = test_value

        mocker.patch('server.FileBasedKeyValueStore', return_value=mock_store)

        request_body = GetValueRequestBody(key=test_key, user=test_user)

        # Act
        result = get_value(request_body)

        # Assert
        assert result == {"key": test_key, "value": test_value}
        mock_store.get.assert_called_once_with(test_key)

    # Return None for non-existent key
    def test_get_value_returns_none_for_missing_key(self, mocker):
        # Arrange
        test_key = "nonexistent_key"

        mock_store = mocker.Mock()
        mock_store.get.return_value = None

        mocker.patch('server.FileBasedKeyValueStore', return_value=mock_store)

        request_body = GetValueRequestBody(key=test_key, user=test_user)

        # Act
        result = get_value(request_body)

        # Assert
        assert result == {"key": test_key, "value": None}
        mock_store.get.assert_called_once_with(test_key)
