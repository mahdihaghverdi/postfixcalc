import ast
from shlex import shlex
from typing import NoReturn

import black

ops = {"+", "-", "*", "/", "(", ")", "^"}

priorities = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "^": 3,
    "(": 4,
}


def _syntax_check(expression: str) -> bool | NoReturn:
    """Check the syntax of entered expression"""
    return bool(
        ast.parse(expression.translate(str.maketrans({"^": "**"}))),  # type: ignore
    )


def _black_format(expression: str) -> str | NoReturn:
    """Reformat the expression based on PEP8"""
    if _syntax_check(expression):
        return black.format_str(
            expression.replace("^", "**"),
            mode=black.Mode(),
        ).replace("**", "^")
    return ""


def _concat_dotted_numbers(expression: str) -> list[str]:
    """Return a concat nums with fraction dots"""
    # 2. [..., '1', '.', '1', ...] -> [..., '1.1', ...]
    stack: list[str] = []
    for char in shlex(expression):
        if stack and (char.isdigit() and stack[-1] == "."):
            stack.pop()
            left = stack.pop()
            stack.append(f"{left}.{char}")
        else:
            stack.append(char)
    return stack


def _make_num(postfix: list[str]) -> list[str | int | float]:
    """Make numbers int | float and return the postfix list"""
    new_list = []
    num_or_op: str | int | float
    for num_or_op in postfix:
        try:
            num_or_op = float(num_or_op)
        except ValueError:
            pass
        else:
            if num_or_op.is_integer():
                num_or_op = int(num_or_op)
        new_list.append(num_or_op)
    return new_list


def _concat_unary_minus(postfix: list[str]) -> list[str | int | float]:
    """Apply unary minus to numbers

    e.g.
    make all [..., NUMBER, '-', ...] to this: [..., -NUMBER, ...]
    """
    postfix = _make_num(postfix)  # type: ignore
    stack: list[int | float | str] = []
    for item in postfix:
        if isinstance(item, (int, float)):
            stack.append(item)
        elif item == "-":
            if isinstance(stack[-1], (int, float)):
                last = stack.pop()
                if not stack:
                    stack.append(_make_num(["-" + str(last)])[0])
                else:
                    stack.append(last)
                    stack.append(item)
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


def infix_to_postfix(expression: str) -> list[str | int | float]:
    """Return a list of strings but ordered in postfix

    This function DOES care about unary minus, e.g. -1
    """
    ops_stack, postfix = [], []
    for character in _concat_dotted_numbers(_black_format(expression)):
        if character not in ops:
            postfix.append(character)
        elif character == "(":
            ops_stack.append("(")
        elif character == ")":
            while ops_stack and ops_stack[-1] != "(":
                postfix.append(ops_stack.pop())
            ops_stack.pop()
        else:
            while (
                ops_stack
                and ops_stack[-1] != "("
                and priorities[character] <= priorities[ops_stack[-1]]
            ):
                postfix.append(ops_stack.pop())
            ops_stack.append(character)
    while ops_stack:
        postfix.append(ops_stack.pop())
    return _concat_unary_minus(postfix)
