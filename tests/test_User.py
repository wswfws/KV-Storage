import hashlib

from Models.User import User


class TestUser:

    # Verify get_user_filename returns correct SHA256 hash for standard alphanumeric user_id
    def test_get_user_filename_returns_correct_hash(self):
        # Arrange
        test_user = User(user_id="abc123", password_hash="dummy_hash")
        expected_hash = "6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090"

        # Act
        result = test_user.get_user_filename()

        # Assert
        assert result == expected_hash

    # Test get_user_filename with empty user_id string
    def test_get_user_filename_with_empty_user_id(self):
        # Arrange
        test_user = User(user_id="", password_hash="dummy_hash")
        expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

        # Act
        result = test_user.get_user_filename()

        # Assert
        assert result == expected_hash

    # Check that get_user_filename output is always 64 characters long
    def test_get_user_filename_length(self):
        # Arrange
        test_user = User(user_id="abc123", password_hash="dummy_hash")

        # Act
        result = test_user.get_user_filename()

        # Assert
        assert len(result) == 64

    # Validate that same user_id consistently produces same filename hash
    def test_get_user_filename_consistent_hash(self):
        # Arrange
        user_id = "consistent_user"
        test_user = User(user_id=user_id, password_hash="dummy_hash")
        expected_hash = hashlib.sha256(user_id.encode()).hexdigest()

        # Act
        first_result = test_user.get_user_filename()
        second_result = test_user.get_user_filename()

        # Assert
        assert first_result == expected_hash
        assert second_result == expected_hash
        assert first_result == second_result
