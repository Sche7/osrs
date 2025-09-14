import pytest

from src.runescape.api.osrs.hiscores import Hiscores


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


@pytest.mark.parametrize("username", ["Zehahandsome"])
def test_hiscores(username: str):
    """Test the get_character_stats method."""
    hiscores = Hiscores(username)

    # Since the character stats are always changing, we can't really test
    # for a specific value. We can however test that the values are greater
    # than a certain value. We test that the values are greater than 1,
    # since sometimes the hiscores may not appear in the database when
    # the user has not logged in for a while.
    assert hiscores.character.combat_level >= 1
    assert hiscores.character.total_level >= 1
    assert hiscores.character.username == username


def test_hiscores_invalid_username():
    """Test the get_character_stats method with an invalid username."""
    username = "ThisIsAnInvalidUsername1231456"
    with pytest.raises(ValueError, match=f"User {username} does not exist."):
        Hiscores(username)
