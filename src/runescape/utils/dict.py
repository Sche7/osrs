from collections.abc import MutableMapping
from typing import Any


def flatten(
    dictionary,
    parent_key: str = "",
    separator: str = ".",
) -> dict[str, Any]:
    """
    Flatten a dictionary with a separator.
    This is the inverse of unflatten.

    Example:
    >>> flatten({"a": 1, "b": {"c": 2, "d": {"e": 3, "f": 4}, "g": 5}})
    {"a": 1, "b.c": 2, "b.d.e": 3, "b.d.f": 4, "b.g": 5}

    """
    items = []
    for key, value in dictionary.items():
        new_key = parent_key + separator + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten(value, new_key, separator=separator).items())
        else:
            items.append((new_key, value))
    return dict(items)


def unflatten(dictionary, separator: str = ".") -> dict[str, Any]:
    """
    Unflatten a dictionary with a separator.
    This is the inverse of flatten.

    Example:
    >>> unflatten({"a": 1, "b.c": 2, "b.d.e": 3, "b.d.f": 4, "b.g": 5})
    {"a": 1, "b": {"c": 2, "d": {"e": 3, "f": 4}, "g": 5}}
    """
    items = {}
    for key, value in dictionary.items():
        parts = key.split(separator)
        d = items
        for part in parts[:-1]:
            if part not in d:
                d[part] = {}
            d = d[part]
        d[parts[-1]] = value
    return items
