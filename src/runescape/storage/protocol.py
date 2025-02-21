from typing import Any, Protocol


class StorageProtocol(Protocol):
    def save(self, data: Any, key: str) -> Any: ...

    def load(self, key: str) -> Any: ...
