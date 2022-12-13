from operator import add, mul, sub, truediv

from . import infix_to_postfix
from .typings import ListExpression

eval_ops = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truediv,
    "^": pow,
}


def _evaluate(postfix: "ListExpression") -> int | float:
    """Simple postfix notation evaluate function"""
    res = 0
    eval_stack = []
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


def evaluate(expression: str) -> int | float:
    return _evaluate(infix_to_postfix(expression))
