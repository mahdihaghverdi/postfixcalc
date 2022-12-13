from postfixcalc import _make_num


def test_make_num():
    assert _make_num(["1", "1.1", "^"]) == [1, 1.1, "^"]
