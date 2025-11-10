from urllib.parse import urlencode, urlunparse

import httpx

from runescape.api.osrs.models import Alpha, Categories
from runescape.api.utils import UrlComponents


class OSRSItemsModule:
    scheme = "https"
    base_url = "secure.runescape.com"
    path = "/m=itemdb_rs/api/catalogue/items.json"

    def browse(
        self,
        category: Categories,
        alpha: Alpha,
        page: int,
    ):
        params = {
            "category": category.value.id,
            "alpha": alpha,
            "page": page,
        }

        url = urlunparse(
            UrlComponents(
                scheme=self.scheme,
                netloc=self.base_url,
                path=self.path,
                params="",
                query=urlencode(params),
                fragment="",
            )
        )
        response = httpx.get(url)
        response.raise_for_status()
        return response
