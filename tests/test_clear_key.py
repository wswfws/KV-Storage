from Models.User import UserModel

from server import clear_key, ClearKeyRequestBody


class TestClearKey:

    # Clear existing key and receive OK status response
    def test_clear_existing_key_returns_ok(self, mocker):
        # Arrange
        test_key = "nonexistent_key"
        test_user = UserModel(user_id="test_user", password_hash="a" * 64)

        mock_store = mocker.Mock()
        mock_store.get.return_value = None

        mocker.patch('server.FileBasedKeyValueStore', return_value=mock_store)

        request_body = ClearKeyRequestBody(key=test_key, user=test_user)

        # Act
        result = clear_key(request_body)

        # Assert
        assert result == {"status": "OK"}
        mock_store.delete.assert_called_once_with(test_key)
