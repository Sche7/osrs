import json
from core.storage.protocol import StorageProtocol


class JSONStorage(StorageProtocol):
    def save(self, data, filepath: str):
        with open(filepath, "w") as file:
            json.dump(data, file)
        return filepath

    def load(self, filepath: str):
        with open(filepath, "r") as file:
            return json.load(file)
