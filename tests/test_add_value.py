import pytest

from Models.User import UserModel, convert_user_model_to_user
from server import add_value, buffer_store, AddValueRequestBody
from storage.FileBasedKeyValueStore import FileBasedKeyValueStore

class TestAddValue:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Clear the buffer and storage before each test."""
        buffer_store.clear()
        user = UserModel(user_id="test_user", password_hash="a" * 64)
        store = FileBasedKeyValueStore(convert_user_model_to_user(user).get_user_filename())
        store.store.clear()
        store._save_data()

    # Adding first part of value returns IN_PROGRESS status
    def test_add_first_part_returns_in_progress(self):
        # Arrange
        user = UserModel(user_id="test_user", password_hash="a" * 64)
        request = AddValueRequestBody(
            key="test_key",
            value="part1",
            finish_value=False,
            user=user
        )

        # Act
        result = add_value(request)

        # Assert
        assert result["status"] == "IN_PROGRESS"

    # Empty value string in request
    def test_empty_value_string_handled(self):
        # Arrange
        user = UserModel(user_id="test_user", password_hash="a" * 64)
        request = AddValueRequestBody(
            key="test_key",
            value="",
            finish_value=False,
            user=user
        )

        # Act
        result = add_value(request)

        # Assert
        assert result["status"] == "IN_PROGRESS"
        buffer_key = f"{convert_user_model_to_user(user).get_user_filename()}:test_key"
        assert buffer_store[buffer_key] == ""

    # Adding final part with finish_value=true stores complete value and returns OK status
    def test_add_final_part_returns_ok(self):
        # Arrange
        user = UserModel(user_id="test_user", password_hash="a" * 64)
        request = AddValueRequestBody(
            key="test_key",
            value="final_part",
            finish_value=True,
            user=user
        )
        buffer_key = f"{convert_user_model_to_user(user).get_user_filename()}:{request.key}"
        buffer_store[buffer_key] = "initial_part"

        # Act
        result = add_value(request)

        # Assert
        assert result["status"] == "OK"
        store = FileBasedKeyValueStore(convert_user_model_to_user(user).get_user_filename())
        assert store.get(request.key) == ["initial_partfinal_part"]

    # Multiple partial values are correctly concatenated in buffer
    def test_multiple_partial_values_concatenation(self):
        # Arrange
        user = UserModel(user_id="test_user", password_hash="a" * 64)
        request1 = AddValueRequestBody(
            key="test_key",
            value="part1",
            finish_value=False,
            user=user
        )
        request2 = AddValueRequestBody(
            key="test_key",
            value="part2",
            finish_value=False,
            user=user
        )
        request3 = AddValueRequestBody(
            key="test_key",
            value="part3",
            finish_value=True,
            user=user
        )

        # Act
        result1 = add_value(request1)
        result2 = add_value(request2)
        result3 = add_value(request3)

        # Assert
        assert result1["status"] == "IN_PROGRESS"
        assert result2["status"] == "IN_PROGRESS"
        assert result3["status"] == "OK"
