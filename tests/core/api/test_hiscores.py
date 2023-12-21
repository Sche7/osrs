import pytest
from core.api.hiscores import Hiscores


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
    """Test the combat level calculation."""
    assert (
        Hiscores.calculate_combat_level(
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


@pytest.mark.parametrize("username", ["NotCrostyGIM", "Zehahandsome"])
def test_get_character_stats(username: str):
    """Test the get_character_stats method."""
    hiscores = Hiscores(username)

    # Since the character stats are always changing, we can't really test
    # for a specific value. We can however test that the values are greater
    # than a certain value. As these characters exists, we can assume that
    # they will always have a combat level greater than 3 and a total level
    # greater than 32.
    assert hiscores.character.combat_level > 3
    assert hiscores.character.total_level > 32
    assert hiscores.character.username == username
