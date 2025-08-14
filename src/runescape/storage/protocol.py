from typing import Any, Protocol


class StorageProtocol(Protocol):
    """Protocol for storage classes."""

    def save(self, data: Any, key: str) -> Any:
        """
        Save data to a storage.
        """

    def load(self, key: str) -> Any:
        """
        Load data from a storage.
        """
