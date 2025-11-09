import requests

from runescape.api.osrs import HiscoreType
from runescape.dataclasses.player import Player


class HiscoresJSON:
    def __init__(self, username, hiscore_type: HiscoreType = HiscoreType.NORMAL):
        self.username = username
        self.hiscore_type = hiscore_type

    @property
    def url(self):
        return (
            f"https://secure.runescape.com/m={self.hiscore_type.value}/"
            f"index_lite.json?player={self.username}"
        )

    def get(self) -> Player:
        response = requests.get(self.url)
        if response.status_code == 404:
            raise ValueError(f"User {self.username} does not exist.")
        if response.status_code != 200:
            raise ValueError(f"Error {response.status_code} when scraping {self.url}")
        return Player(**response.json())
