import pytest
from core.scrapers.character_stats import CharacterStats


@pytest.mark.parametrize(
    (
        "attack",
        "strength",
        "defence",
        "hitpoints",
        "prayer",
        "ranged",
        "magic",
        "expected",
    ),
    [
        (
            40,
            40,
            36,
            38,
            26,
            26,
            32,
            47,
        ),
        (
            1,
            1,
            1,
            10,
            1,
            1,
            1,
            3,
        ),
    ],
)
def test_calculate_combat_level(
    attack: int,
    strength: int,
    defence: int,
    hitpoints: int,
    prayer: int,
    ranged: int,
    magic: int,
    expected: int,
):
    scraper = CharacterStats("Test")
    assert (
        scraper.calculate_combat_level(
            attack,
            strength,
            defence,
            hitpoints,
            prayer,
            ranged,
            magic,
        )
        == expected
    )
