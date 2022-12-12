import pathlib
import sys
from shlex import shlex

sys.path += [str(pathlib.Path(__file__).parent.parent.parent)]
from plumacalc import _concat_dotted_numbers  # noqa


def test_concat_dotted_numbers():
    stmt = ".1"
    assert _concat_dotted_numbers(stmt) == ["0.1"]

    stmt = "1.2"
    assert _concat_dotted_numbers(stmt) == ["1.2"]

    stmt = "2 ^ .1 * 4 + 1"
    expected = list(shlex(stmt))
    del expected[2]
    expected[2] = "0.1"
    assert _concat_dotted_numbers(stmt) == expected

    stmt = "2 ^ 1.3 * 4 + 1"
    expected = list(shlex(stmt))
    del expected[2:4]
    expected[2] = "1.3"
    print(expected)
    assert _concat_dotted_numbers(stmt) == expected
