import pytest

from runescape.api.osrs.catalogue import OSRSCatalogue
from runescape.api.osrs.models import Categories
from runescape.dataclasses.items import Items


@pytest.mark.parametrize(
    ("category", "alpha", "page"),
    [
        ("1", "a", 3),
        ("3", "z", 1),
        (Categories.AMMO, "a", 1),
    ],
)
def test_catalogue_items(category, alpha, page):
    client = OSRSCatalogue()
    result = client.items(category=category, alpha=alpha, page=page)
    assert isinstance(result, Items)
