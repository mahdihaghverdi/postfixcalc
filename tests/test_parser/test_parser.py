import pytest

from postfixcalc.ast_parser import parse


def test_syntax_error():

    with pytest.raises(SyntaxError) as e:
        parse("2 +")
        assert "invalid syntax" in e.__str__()

    with pytest.raises(SyntaxError) as e:
        parse("2 + )")
        assert "unmatched" in e.__str__()

    with pytest.raises(SyntaxError) as e:
        parse("( + 3")
        assert "was never closed" in e.__str__()


def test_successful_parse():
    parse("2 ** 4 + - 3")
