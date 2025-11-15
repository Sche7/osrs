import pytest
from httpx import HTTPStatusError

from runescape.api.osrs.grand_exchange import GrandExchangeClient
from runescape.api.osrs.models import Category
from runescape.dataclasses.categories import CategoryOverview
from runescape.dataclasses.items import ItemDetails, Items


@pytest.mark.parametrize(
    ("category", "alpha", "page"),
    [
        (1, "a", 3),
        ("1", "a", "3"),
        (3, "z", 1),
        (Category.AMMO, "a", 1),
    ],
)
def test_grand_exchange_get_items(category, alpha, page):
    client = GrandExchangeClient()
    result = client.get_items(category=category, alpha=alpha, page=page)
    assert isinstance(result, Items)


def test_grand_exchange_get_items_exception():
    client = GrandExchangeClient()

    with pytest.raises(HTTPStatusError):
        client.get_items(
            category=1000,  # Non-existent category
            alpha="a",
            page=1,
        )


@pytest.mark.parametrize(
    "category",
    [
        Category.AMMO,
        Category.ARCHAEOLOGY_MATERIALS,
        Category.ARROWS,
        0,
        1,
        2,
    ],
)
def test_grand_exchange_get_categories(category):
    client = GrandExchangeClient()
    result = client.get_category_overview(category=category)
    assert isinstance(result, CategoryOverview)


@pytest.mark.parametrize("item_id", [21787, 21777, "21787"])
def test_grand_exchange_get_item_details(item_id):
    client = GrandExchangeClient()
    result = client.get_item_details(item_id)
    assert isinstance(result, ItemDetails)


def test_grand_exchange_get_item_details_exception():
    client = GrandExchangeClient()
    with pytest.raises(HTTPStatusError):
        client.get_item_details(0)
