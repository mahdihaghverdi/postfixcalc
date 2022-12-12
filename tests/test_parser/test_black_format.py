from plumacalc import _black_format


def test_black_format():
    assert _black_format(".1 ^ 3 * -1 ^ 3") == "0.1^3 * -(1^3)\n"
