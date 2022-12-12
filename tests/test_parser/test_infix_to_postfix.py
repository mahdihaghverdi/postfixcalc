from plumacalc import infix_to_postfix


def test_infix_to_postfix():
    assert infix_to_postfix("1.1^2+4") == [1.1, 2, "^", 4, "+"]
    assert infix_to_postfix("(-1)^3-4/2^10") == [-1, 3, "^", 4, 2, 10, "^", "/", "-"]
    assert infix_to_postfix("-1 ^ 3 - 4 / 2 ^ 10") == [
        1,
        3,
        "^",
        "-",
        4,
        2,
        10,
        "^",
        "/",
        "-",
    ]
