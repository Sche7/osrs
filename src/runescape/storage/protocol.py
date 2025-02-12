from typing import Any, Protocol


class StorageProtocol(Protocol):
    def save(self) -> Any: ...

    def load(self) -> Any: ...
