from src.utils.dict import flatten, unflatten


def test_flatten():
    d = {"a": 1, "b": {"c": 2, "d": {"e": 3, "f": 4}, "g": 5}}
    assert flatten(d) == {"a": 1, "b.c": 2, "b.d.e": 3, "b.d.f": 4, "b.g": 5}


def test_unflatten():
    d = {"a": 1, "b.c": 2, "b.d.e": 3, "b.d.f": 4, "b.g": 5}
    assert unflatten(d) == {"a": 1, "b": {"c": 2, "d": {"e": 3, "f": 4}, "g": 5}}
