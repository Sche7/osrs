from core.utils.dict import flatten


def test_flatten():
    d = {"a": 1, "b": {"c": 2, "d": {"e": 3, "f": 4}, "g": 5}}
    assert flatten(d) == {"a": 1, "b.c": 2, "b.d.e": 3, "b.d.f": 4, "b.g": 5}
