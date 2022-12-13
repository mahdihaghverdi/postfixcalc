from shlex import shlex

from postfixcalc import _concat_dotted_numbers


def test_concat_dotted_numbers():
    stmt = "1.2"
    assert _concat_dotted_numbers(stmt) == ["1.2"]

    stmt = "2 ^ 1.3 * 4 + 1"
    expected = list(shlex(stmt))
    del expected[2:4]
    expected[2] = "1.3"
    print(expected)
    assert _concat_dotted_numbers(stmt) == expected
