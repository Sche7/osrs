from urllib.parse import urlencode, urlunparse

import httpx

from runescape.api.osrs.models import Alpha, Category
from runescape.api.utils import UrlComponents
from runescape.dataclasses.categories import Tradeables
from runescape.dataclasses.items import Items


class OSRSCatalogue:
    scheme = "https"
    base_url = "secure.runescape.com"
    path = "/m=itemdb_rs/api/catalogue"

    def items(
        self,
        category: Category | int,
        alpha: Alpha,
        page: int,
    ) -> Items:
        params = {
            "category": category.value.id if isinstance(category, Category) else category,
            "alpha": alpha,
            "page": page,
        }

        url = urlunparse(
            UrlComponents(
                scheme=self.scheme,
                netloc=self.base_url,
                path=f"{self.path}/items.json",
                params="",
                query=urlencode(params),
                fragment="",
            )
        )
        response = httpx.get(url)
        response.raise_for_status()
        return Items.model_validate(response.json())

    def categories(self, category: Category | int) -> Tradeables:
        """Returns the number of items determined by the first letter"""
        url = urlunparse(
            UrlComponents(
                scheme=self.scheme,
                netloc=self.base_url,
                path=f"{self.path}/category.json",
                params="",
                query=urlencode(
                    {
                        "category": category.value.id
                        if isinstance(category, Category)
                        else category
                    }
                ),
                fragment="",
            )
        )
        response = httpx.get(url)
        response.raise_for_status()
        return Tradeables.model_validate(response.json())
