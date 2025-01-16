import json

from config import ServerConfig


class FileBasedKeyValueStore:
    def __init__(self, filename='data_store.json'):
        """Load existing data from the file."""
        self.filename = ServerConfig.STORAGE_PATH + filename
        self._load_data()

    def _load_data(self):
        try:
            with open(self.filename, 'r') as file:
                self.store = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.store = {}

    def _save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.store, file)

    def set(self, key, value):
        """Set the value of a key, replacing any existing data."""
        if not isinstance(value, list):
            raise ValueError(f"The value for key '{value}' must be a list.")
        self.store[key] = value
        self._save_data()

    def add(self, key, value):
        """Add a value to the list for a key."""
        if key not in self.store:
            self.store[key] = []
        if not isinstance(self.store[key], list):
            raise ValueError(f"Expected a list for key '{key}', but found {type(self.store[key])}.")
        self.store[key].append(value)
        self._save_data()

    def get(self, key):
        return self.store.get(key, [])

    def delete(self, key):
        if key in self.store:
            del self.store[key]
            self._save_data()
