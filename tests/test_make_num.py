from postfixcalc.ast_parser import make_num


def test_make_num():
    assert make_num(["1", "1.1", "^"]) == [1, 1.1, "^"]
