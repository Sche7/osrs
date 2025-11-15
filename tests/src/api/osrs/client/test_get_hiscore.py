import pytest
from httpx import HTTPStatusError

from runescape.api.osrs.client import OSRSClient
from runescape.dataclasses.player import Player


def test_get_hiscore():
    client = OSRSClient()
    username = "Crosty"
    user_hiscore = client.get_hiscore(username)
    assert isinstance(user_hiscore, Player)
    assert user_hiscore.activities
    assert user_hiscore.skills
    assert user_hiscore.name == username


def test_get_hiscore_non_existing_username():
    client = OSRSClient()
    username = "idonotexist - --"
    with pytest.raises(HTTPStatusError):
        client.get_hiscore(username)
