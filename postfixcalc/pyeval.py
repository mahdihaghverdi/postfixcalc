from functools import cached_property
from numbers import Number
from operator import add, mul, sub, truediv

from .ast_parser import (
    extract_nums_and_ops,
    flatten_nodes,
    infix_to_postfix,
    make_num,
    parse,
    relistexpression,
    restrexpression,
)
from .typings import ListExpression

eval_ops = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truediv,
    "^": pow,
}


def evaluate(postfix: "ListExpression") -> int | float:
    """Simple postfix notation evaluate function"""
    res = 0
    eval_stack = []
    if len(postfix) == 1 and isinstance(postfix[0], Number):
        return postfix[0]

    for num_or_op in postfix:
        if isinstance(num_or_op, (int, float)):
            eval_stack.append(num_or_op)
            continue
        else:
            right = eval_stack.pop()
            try:
                left = eval_stack.pop()
            except IndexError:
                # unary operation
                left = 0 if num_or_op in {"-", "+"} else 1
            res = eval_ops[num_or_op](left, right)  # type: ignore
            eval_stack.append(res)
    return res


class Calc:
    def __init__(self, expr: str):
        self.expr = expr

    @cached_property
    def parsed(self):
        return parse(self.expr)

    @cached_property
    def extracted(self):
        return extract_nums_and_ops(self.parsed)

    @cached_property
    def flattened(self):
        return flatten_nodes(self.extracted)

    @cached_property
    def strparenthesized(self):
        return restrexpression(self.flattened)

    @cached_property
    def listparenthesized(self):
        return relistexpression(self.flattened)

    @cached_property
    def numerized(self):
        return make_num(self.listparenthesized)

    @cached_property
    def postfix(self):
        return infix_to_postfix(self.numerized)

    @cached_property
    def answer(self):
        return evaluate(self.postfix)

    def __repr__(self):
        return f"Calc(expr={self.expr}, answer={self.answer})"
