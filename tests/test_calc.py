import pytest

from postfixcalc import Calc


def test_answer():
    what = "123 + 43 - 8 * 7 ** 2 * - 1 + 2 / 3 ** (1 + 2)"
    c = Calc(what)
    assert c.answer == eval(what)


def test_termination():
    c = Calc("(2 ^ 32) ^ (2 ^ 32)")
    with pytest.raises(TimeoutError) as e:
        print(c.answer)

    assert (
        f"Calculations of {c.strparenthesized!r} took longer than {c.timeout} seconds"
        == f"{e.value}"
    )

    c = Calc("(2 ^ 32) ^ (2 ^ 18)")
    with pytest.raises(TimeoutError):
        print(c.stranswer)
