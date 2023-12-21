from datetime import datetime

from dataclasses import asdict
from core.scrapers.character_stats import CharacterStats
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


def get_single_character_stats(username: str):
    """
    Get the character stats of a given username.

    Parameters
    ----------
    username : str
        The username of the character.

    Returns
    -------
    dict
        The character stats including timestamp.

    """
    scraper = CharacterStats(username)
    character = scraper.get_character_stats()
    dict_character = asdict(character)
    dict_character = flatten(dict_character)

    now = datetime.now()
    now = now.strftime("%Y-%B-%d %H:%M:%S")
    dict_character["timestamp"] = now
    return dict_character


def get_multiple_character_stats(usernames: list[str]):
    """
    Get the character stats of a given list of usernames.

    Parameters
    ----------
    usernames : list
        The list of usernames of the characters.

    Returns
    -------
    list
        The character stats including timestamp.

    """
    characters = []
    for username in usernames:
        character = get_single_character_stats(username)
        characters.append(character)
    return characters
