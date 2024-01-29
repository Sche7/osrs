import json
from runescape.storage.protocol import StorageProtocol


class JSONStorage(StorageProtocol):
    """A class for saving and loading JSON files."""

    def save(self, data: dict, filepath: str) -> str:
        """
        Save JSON data to a file.

        Parameters
        ----------
        data : dict
            The dictionary object to save to JSON file.
        filepath : str
            The path of which to save the file.

        Returns
        -------
        str
            The path of the saved file.

        Examples
        --------
        >>> json_storage = JSONStorage()
        >>> json_storage.save({"foo": "bar"}, "foo.json")
        "foo.json"
        """
        with open(filepath, "w") as file:
            json.dump(data, file)
        return filepath

    def load(self, filepath: str) -> dict:
        """
        Load JSON data from a JSON file.

        Parameters
        ----------
        filepath : str
            The path of which to load the file.

        Returns
        -------
        dict
            The dictionary object loaded from the JSON file.

        Examples
        --------
        >>> json_storage = JSONStorage()
        >>> json_storage.load("foo.json")
        {"foo": "bar"}
        """
        with open(filepath, "r") as file:
            return json.load(file)
