from server import clear_key, ClearKeyRequestBody
from tests.start_test import test_user


class TestClearKey:

    # Clear existing key and receive OK status response
    def test_clear_existing_key_returns_ok(self):
        request_body = ClearKeyRequestBody(key="test_key", user=test_user)

        # Act
        result = clear_key(request_body)

        # Assert
        assert result == {"status": "OK"}
