from collections import namedtuple
from urllib.parse import urlencode, urlunparse

import httpx

from runescape.api.osrs import HiscoreType
from runescape.dataclasses.player import Player

Components = namedtuple(
    typename="Components",
    field_names=["scheme", "netloc", "path", "params", "query", "fragment"],
)


class OSRSClient:
    scheme = "https"
    base_url = "secure.runescape.com"

    def hiscore(
        self,
        username: str,
        hiscore_type: HiscoreType = HiscoreType.NORMAL,
    ) -> Player:
        url = urlunparse(
            Components(
                scheme=self.scheme,
                netloc=self.base_url,
                path=f"/m={hiscore_type.value}/index_lite.json",
                params="",
                query=urlencode({"player": username}),
                fragment="",
            )
        )
        response = httpx.get(url)
        response.raise_for_status()
        return Player.model_validate(response.json())
