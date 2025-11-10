from urllib.parse import urlencode, urlunparse

import httpx

from runescape.api.osrs import HiscoreType
from runescape.api.osrs.catalogue import OSRSCatalogue
from runescape.api.utils import UrlComponents
from runescape.dataclasses.player import Player


class OSRSClient:
    scheme = "https"
    base_url = "secure.runescape.com"

    def hiscore(
        self,
        username: str,
        hiscore_type: HiscoreType = HiscoreType.NORMAL,
    ) -> Player:
        url = urlunparse(
            UrlComponents(
                scheme=self.scheme,
                netloc=self.base_url,
                path=f"/m={hiscore_type.value}/index_lite.json",
                params="",
                query=urlencode({"player": username}),
                fragment="",
            )
        )
        response = httpx.get(url.decode())
        response.raise_for_status()
        return Player.model_validate(response.json())

    @property
    def catalogue(self) -> OSRSCatalogue:
        return OSRSCatalogue()
