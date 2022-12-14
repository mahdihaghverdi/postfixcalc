import pytest

from postfixcalc import _parse


def test_syntax_error():

    with pytest.raises(SyntaxError) as e:
        _parse("2 +")
        assert "invalid syntax" in e.__str__()

    with pytest.raises(SyntaxError) as e:
        _parse("2 + )")
        assert "unmatched" in e.__str__()

    with pytest.raises(SyntaxError) as e:
        _parse("( + 3")
        assert "was never closed" in e.__str__()


def test_successful_parse():
    _parse("2 ** 4 + - 3")
