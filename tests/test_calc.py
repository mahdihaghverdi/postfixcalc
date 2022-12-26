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
        f"Calculations of {c.expr!r} took longer than {c.calc_timeout} seconds"
        == f"{e.value}"
    )

    c = Calc("(2 ^ 32) ^ (2 ^ 15)")
    with pytest.raises(expected_exception=(TimeoutError, ValueError)) as e:  # noqa
        print(c.stranswer())

    assert (
        f"Generating a string representation of {c.expr!r} "
        f"took longer than {c.str_repr_timeout} seconds"
    ) == f"{e.value}"

    c = Calc("(2 ^ 32) ^ (2 ^ 18)", calc_timeout=2, str_repr_timeout=4)
    with pytest.raises(expected_exception=(TimeoutError, ValueError)) as e:  # noqa
        print(c.stranswer())

    assert (
        f"Generating a string representation of {c.strparenthesized!r} "
        f"took longer than {c.str_repr_timeout} seconds"
    ) == f"{e.value}"


def test_stranswer():
    calc = Calc("(2 ^ 32) ^ (2 ^ 15)", calc_timeout=1, str_repr_timeout=2)
    assert calc.stranswer(5) == "67411..."
    assert calc.stranswer(ending=5) == "...79136"
    assert calc.stranswer(5, 5) == "67411...79136"
