import hashlib


class ServerConfig:
    STORAGE_PATH = "C:\\Users\\gelli\\PycharmProjects\\KV-Storage\\storage\\"
    ACSEPT_USERS = [
        {
            "user_id": "1",
            "password_hash": hashlib.sha256("password".encode()).hexdigest()
        },
        {
            "user_id": "2",
            "password_hash": hashlib.sha256("password2".encode()).hexdigest()
        },
        {
            "user_id": "test_user_id",
            "password_hash": hashlib.sha256("test_password_hash".encode()).hexdigest()
        }
    ]


class ClientConfig:
    SERVER_ADRRS = ["http://localhost:8000", "http://localhost:8001"]
    USER = {
        "user_id": "1",
        "password_hash": hashlib.sha256("password".encode()).hexdigest()
    }
