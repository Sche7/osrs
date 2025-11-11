import pytest
from httpx import HTTPStatusError

from runescape.api.osrs.catalogue import OSRSCatalogue
from runescape.api.osrs.models import Categories
from runescape.dataclasses.categories import Tradeables
from runescape.dataclasses.items import Items


@pytest.mark.parametrize(
    ("category", "alpha", "page"),
    [
        (1, "a", 3),
        ("1", "a", "3"),
        (3, "z", 1),
        (Categories.AMMO, "a", 1),
    ],
)
def test_catalogue_items(category, alpha, page):
    client = OSRSCatalogue()
    result = client.items(category=category, alpha=alpha, page=page)
    assert isinstance(result, Items)


def test_catalogue_items_exception():
    client = OSRSCatalogue()

    with pytest.raises(HTTPStatusError):
        client.items(
            category=1000,  # Non-existence category
            alpha="a",
            page=1,
        )


@pytest.mark.parametrize(
    "category",
    [
        Categories.AMMO,
        Categories.ARCHAEOLOGY_MATERIALS,
        Categories.ARROWS,
        0,
        1,
        2,
    ],
)
def test_catalogue_categories(category: Categories):
    client = OSRSCatalogue()
    result = client.categories(category=category)
    assert isinstance(result, Tradeables)
