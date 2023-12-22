from collections.abc import MutableMapping


def flatten(dictionary, parent_key="", separator="."):
    items = []
    for key, value in dictionary.items():
        new_key = parent_key + separator + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten(value, new_key, separator=separator).items())
        else:
            items.append((new_key, value))
    return dict(items)


def unflatten(dictionary, separator="."):
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
