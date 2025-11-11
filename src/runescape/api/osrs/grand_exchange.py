from urllib.parse import urlencode, urlunparse

import httpx

from runescape.api.osrs.models import Alpha, Category
from runescape.api.utils import UrlComponents
from runescape.dataclasses.categories import CategoryOverview
from runescape.dataclasses.items import Items


class GrandExchangeClient:
    scheme = "https"
    base_url = "secure.runescape.com"
    path = "/m=itemdb_rs/api/catalogue"

    def get_items(
        self,
        category: Category | int,
        alpha: Alpha,
        page: int,
    ) -> Items:
        """Get a list of items filtered by category, alpha and page.

        Parameters
        ----------
        category: Category | int
            The type of items to search for. There are 44 categories
            starting with category 0 to 43.
            Use either integers or the enum
            runescape.api.osrs.models.Category for better overview
            of categories.
        alpha: Alpha
            The starting letter or number of item name to filter by.
            Note that any items that start with a number must instead use %23 instead of #.
        page: int
            The page number to retrieve. Each page include 10 items.
        """
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

    def get_category_overview(self, category: Category | int) -> CategoryOverview:
        """Get an overview of number of tradeable items within a certain category.

        Returns the number of items determined by the first letter.

        Parameters
        ----------
        category: Category | int
            The type of items to search for. There are 44 categories
            starting with category 0 to 43.
            Use either integers or the enum
            runescape.api.osrs.models.Category for better overview
            of categories.

        """
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
        return CategoryOverview.model_validate(response.json())
