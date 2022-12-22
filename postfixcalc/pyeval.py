import multiprocessing
from functools import cached_property
from numbers import Number
from operator import add, mul, sub, truediv

from .parser import (
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
    def __init__(self, expr: str, timeout: int | float = 0.1):
        self.expr = expr
        self.timeout = timeout

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
        """Calculate the answer respecting the `timeout`

        IMPORTANT NOTE: DON'T CALL `print` ON THE RESULT OF THIS METHOD
        This is because for instance calculating `(2 ^ 32) ^ (2 ^ 18)` is done under `timeout` BUT generating the str
        repr WILL TAKE MUCH LONGER!!!

        If you want to `print` the result, use `stranswer` method
        """
        process = multiprocessing.Process(target=evaluate, args=(self.postfix,))
        process.start()
        process.join(timeout=self.timeout)
        if process.is_alive():
            process.terminate()
            raise TimeoutError(
                f"Calculations of {self.strparenthesized!r} took longer than {self.timeout} seconds",
            ) from None
        return evaluate(self.postfix)

    @cached_property
    def stranswer(self) -> str:
        process = multiprocessing.Process(target=str, args=(self.answer,))
        process.start()
        process.join(self.timeout * 2)
        if process.is_alive():
            process.terminate()
            raise TimeoutError(
                f"Generating a string representation of {self.strparenthesized!r} took longer than {self.timeout} seconds",
            ) from None
        try:
            return str(self.answer)
        except ValueError:
            raise TimeoutError(
                f"Generating a string representation of {self.strparenthesized!r} took longer than {self.timeout} seconds",
            ) from None

    def __repr__(self):
        return f"Calc(expr={self.expr}, answer={self.answer})"
