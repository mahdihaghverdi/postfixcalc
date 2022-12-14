import math

from postfixcalc.ast_parser import (
    extract_nums_and_ops,
    flatten_nodes,
    infix_to_postfix,
    make_num,
    parse,
    relistexpression,
)
from postfixcalc.pyeval import evaluate


def test_evaluate():
    to_evals: dict[str, int | float] = {
        "-1 ** 3": -1,
        "2 - 4 ** 2": -14,
        "0.1 + 0.1 - 0.1": 0.1,
        "3 * 6 - 9 + 6 ** 4 / 8 * 7 + (-4)": 1139.0,
        "1 * (2 / (2 ** (-1 + 2 * -1))) ** 3": 4096.0,
        "123 + 43 - 8 * 7 ** 2 * - 1 + 2 / 3 ** (1 + 2)": 558.074074074074,
    }
    for expr, answer in to_evals.items():
        assert math.isclose(
            eval(expr),
            evaluate(
                infix_to_postfix(
                    make_num(
                        relistexpression(
                            flatten_nodes(
                                extract_nums_and_ops(parse(expr.replace("**", "^"))),
                            ),
                        ),
                    ),
                ),
            ),
        )
