from urllib.parse import urlencode, urlunparse

import httpx

from runescape.api.osrs import HiscoreType
from runescape.api.osrs.catalogue import OSRSCatalogue
from runescape.api.utils import UrlComponents
from runescape.dataclasses.player import Player


class OSRSClient:
    """Class that wraps the OSRS API endpoints.

    This uses the official hiscores API from Jagex.
    See also: https://runescape.wiki/w/Application_programming_interface#Old_School_Hiscores
    """

    scheme = "https"
    base_url = "secure.runescape.com"

    def hiscore(
        self,
        username: str,
        hiscore_type: HiscoreType = HiscoreType.NORMAL,
    ) -> Player:
        """
        Retrieve hiscore of a OSRS user.

        Parameters
        ----------
        username: str
            Name of the user account
        hiscore_type: HiscoreType, optional
            The type of hiscore to look for. By default,
            HiscoreType.NORMAL which is the hiscore for normal
            OSRS users. Other options are:
                - HiscoreType.IRONMAN
                - HiscoreType.ULTIMATE
                - HiscoreType.HARDCORE
                - HiscoreType.DEADMAN
                - HiscoreType.SEASONAL
                - HiscoreType.TOURNAMENT
        """
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
        response = httpx.get(url)
        response.raise_for_status()
        return Player.model_validate(response.json())

    @property
    def catalogue(self) -> OSRSCatalogue:
        return OSRSCatalogue()
