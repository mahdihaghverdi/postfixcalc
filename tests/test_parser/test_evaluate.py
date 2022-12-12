from plumacalc import evaluate, infix_to_postfix


def test_evaluate():
    to_evals: dict[str, int | float] = {
        "-1 ** 3": -1,
        "2 - 4 ** 2": -14,
        "0.1 + 0.1 - 0.1": 0.1,
        "3 * 6 - 9 + 6 ** 4 / 8 * 7 + (-4)": 1139.0,
    }
    for expr, answer in to_evals.items():
        # print(expr, answer, type(expr))
        assert eval(expr) == evaluate(infix_to_postfix(expr.replace("**", "^")))
