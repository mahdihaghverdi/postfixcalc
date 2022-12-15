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
    to_evals = [
        "-1 ** 3",
        "2 - 4 ** 2",
        "0.1 + 0.1 - 0.1",
        "3 * 6 - 9 + 6 ** 4 / 8 * 7 + (-4)",
        "1 * (2 / (2 ** (-1 + 2 * -1))) ** 3",
        "123 + 43 - 8 * 7 ** 2 * - 1 + 2 / 3 ** (1 + 2)",
        "-(-1 - 3)",
        "--(-1 -3)"
    ]
    for expr in to_evals:
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
            rel_tol=0.001
        )
