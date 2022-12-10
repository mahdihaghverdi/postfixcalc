import ast
from shlex import shlex
from typing import NoReturn

from plumacalc.typings import ParsedPostfix, RawPostfix

ops = {"+", "-", "*", "/", "(", ")", "^"}

priorities = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "^": 3,
}


def syntax_check(expression: str) -> bool | NoReturn:
    return bool(
        ast.parse(expression.translate(str.maketrans({"^": "**"}))),  # type: ignore
    )


def infix_to_postfix(expression: str) -> "RawPostfix":
    """Return a list of strings but ordered in postfix

    This function does not care about unary ops, e.g. -1 or +1
    """
    ops_stack, digits_stack = [], []
    for character in shlex(expression):
        if character not in ops:
            digits_stack.append(character)
        elif character == "(":
            ops_stack.append("(")
        elif character == ")":
            while ops_stack and ops_stack[-1] != "(":
                digits_stack.append(ops_stack.pop())
            ops_stack.pop()
        else:
            while (
                ops_stack
                and ops_stack[-1] != "("
                and priorities[character] <= priorities[ops_stack[-1]]
            ):
                digits_stack.append(ops_stack.pop())
            ops_stack.append(character)
    while ops_stack:
        digits_stack.append(ops_stack.pop())
    return digits_stack


def _inter(postfix: "RawPostfix") -> "ParsedPostfix":
    """Make numbers int and return the postfix list"""
    new_list: "ParsedPostfix" = []
    for num_or_op in postfix:
        try:
            num_or_op = int(num_or_op)  # type: ignore
        except ValueError:
            pass
        new_list.append(num_or_op)
    return new_list


def concat_unary_minus(postfix: "RawPostfix") -> "ParsedPostfix":
    """Apply unary minus to numbers

    e.g.
    make all [..., NUMBER, '-', ...] to this: [..., -NUMBER, ...]
    """
    postfix = _inter(postfix)  # type: ignore
    stack: "ParsedPostfix" = []
    for item in postfix:
        if isinstance(item, int):
            stack.append(item)
        elif item == "-":
            if isinstance(stack[-1], int):
                last = stack.pop()
                stack.append(int("-" + str(last)))
            else:
                stack.append(item)
        else:
            stack.append(item)

    if isinstance(stack[-1], (int, float)):
        raise SyntaxError(
            "You have probably written sth like this: `n * -m`. "
            "For this cases you must write: `n * (-m)`",
        )
    return stack


print(concat_unary_minus(infix_to_postfix("2 * -1")))
