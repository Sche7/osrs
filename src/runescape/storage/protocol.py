from typing import Protocol, Any


class StorageProtocol(Protocol):
    def save(self) -> Any:
        ...

    def load(self) -> Any:
        ...
