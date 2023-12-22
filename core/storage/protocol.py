from typing import Protocol, Any


class StorageProtocol(Protocol):
    def save(self, data, filepath: str) -> Any:
        ...

    def load(self, filepath: str) -> Any:
        ...
