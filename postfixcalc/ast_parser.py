import ast
import typing
from collections.abc import Iterable, Sequence
from typing import Union, cast

import black

from .typings import ListExpression, ListPostfix, TupleExpression, ast_ops

operators_names: dict[ast_ops, str] = {
    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.Div: "/",
    ast.Pow: "^",
    ast.USub: "-",
    ast.UAdd: "+",
}

ops: set[str] = {"+", "-", "*", "/", "(", ")", "^"}

priorities: dict[str, int] = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "^": 3,
    "(": 4,
}


def _parse(expression: str) -> "ast.expr":
    """Parse a string expression into ast.expr type"""
    return ast.parse(expression.strip().replace("^", "**"), mode="eval").body


@typing.no_type_check
def _extract_nums_and_ops(node: "ast.expr") -> "ListExpression":
    """Extract numbers, and operators from the parsed expression"""
    stack: "ListExpression" = []
    if isinstance(node, ast.Num):  # <number>
        stack.append(node.n)
    elif isinstance(node, ast.UnaryOp):  # <operator> <number>
        stack.append((node.op, _extract_nums_and_ops(node.operand)))
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        stack.append(
            (
                _extract_nums_and_ops(node.left),
                node.op,
                _extract_nums_and_ops(node.right),
            ),
        )
    else:
        raise TypeError(node)
    return stack


@typing.no_type_check
def _tuplize_nodes(
    nums_and_ops: Union["ListExpression", Sequence],
) -> "TupleExpression":
    """Make anything be a tuple, just to be convenient"""
    to_ret = []
    for thing in nums_and_ops:
        # for [number] case
        if (
            isinstance(thing, list)
            and len(thing) == 1
            and isinstance(thing[0], (int, float))
        ):
            to_ret.append(thing)
        elif isinstance(thing, Sequence):
            to_ret.append(tuple(_tuplize_nodes(thing)))
        else:
            to_ret.append(thing)
    return tuple(to_ret)


@typing.no_type_check
def _flatten_nodes(nums_and_ops: "ListExpression") -> "TupleExpression":
    """Flatten the extracted numbers and operators"""
    stack = []
    for thing in nums_and_ops[0]:
        # for [number] case
        if (
            isinstance(thing, list)
            and len(thing) == 1
            and isinstance(thing[0], (int, float))
        ):
            stack.append(thing)
        elif isinstance(thing, Iterable):
            stack.extend(thing)
        else:
            stack.append(thing)
    return _tuplize_nodes(stack)


@typing.no_type_check
def _restrexpression(flattened: list | tuple) -> str:
    """Generate the str repr of the parsed expression, This is just for visual aspects

    It reformats the generated expression with `black.format_str`
    """
    what = ""
    for listnum_op_tuple in flattened:
        if isinstance(listnum_op_tuple, list) and isinstance(
            listnum_op_tuple[0],
            (int, float),
        ):
            what += str(listnum_op_tuple[0])
        elif isinstance(listnum_op_tuple, ast.AST):
            what += operators_names[type(cast(ast_ops, listnum_op_tuple))]
        else:
            what += "(" + _restrexpression(listnum_op_tuple) + ")"
    return black.format_str(mode=black.Mode(), src_contents=what)


@typing.no_type_check
def _make_num(postfix: "ListPostfix") -> "ListPostfix":
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


@typing.no_type_check
def _relistexpression(flattened: list | tuple) -> "ListPostfix":
    """Generate a parenthesized and typed expression"""
    what = []
    for num_op_tuple in flattened:
        if isinstance(num_op_tuple, list) and isinstance(num_op_tuple[0], (int, float)):
            what.append(num_op_tuple[0])
        elif isinstance(num_op_tuple, ast.AST):
            what.append(operators_names[type(cast(ast_ops, num_op_tuple))])
        else:
            what.append("(")
            got = _relistexpression(num_op_tuple)
            if len(got) == 2:  # for unary ops :-)))
                got = _restrexpression(num_op_tuple)
                what.append(got.strip())
            else:
                what.extend(got)
            what.append(")")
    return what


@typing.no_type_check
def infix_to_postfix(expr: str) -> "ListPostfix":
    """A two stack solution to generate a postfix expression out of an infix expression"""
    expression = _make_num(
        _relistexpression(_flatten_nodes(_extract_nums_and_ops(_parse(expr)))),
    )
    ops_stack: list[str] = []
    postfix: "ListPostfix" = []
    for character in expression:
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
    return postfix
