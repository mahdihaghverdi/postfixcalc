import multiprocessing
from functools import cached_property

from .parser import (
    extract_nums_and_ops,
    flatten_nodes,
    infix_to_postfix,
    make_num,
    parse,
    relistexpression,
    restrexpression,
)
from .pyeval import evaluate


class Calc:
    def __init__(
        self,
        expr: str,
        calc_timeout: int | float = 0.1,
        str_repr_timeout: int | float = 0.2,
    ):
        self.expr = expr
        self.calc_timeout = calc_timeout
        self.str_repr_timeout = str_repr_timeout

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
        """Calculate the answer respecting the `calc_timeout`

        IMPORTANT NOTE: DON'T CALL `print` ON THE RESULT OF THIS METHOD
        This is because for instance calculating `(2 ^ 32) ^ (2 ^ 18)` is done under `timeout` BUT generating the str
        repr WILL TAKE MUCH LONGER!!!

        If you want to `print` the result, use `stranswer` method
        """
        process = multiprocessing.Process(target=evaluate, args=(self.postfix,))
        process.start()
        process.join(timeout=self.calc_timeout)
        if process.is_alive():
            process.terminate()
            raise TimeoutError(
                f"Calculations of {self.strparenthesized!r} took longer than {self.calc_timeout} seconds",
            ) from None
        return evaluate(self.postfix)

    @cached_property
    def stranswer(self) -> str:  # add slicing support
        process = multiprocessing.Process(target=str, args=(self.answer,))
        process.start()
        process.join(self.str_repr_timeout)
        if process.is_alive():
            process.terminate()
            raise TimeoutError(
                f"Generating a string representation of {self.expr!r} took longer than {self.str_repr_timeout} seconds",
            ) from None
        try:
            return str(self.answer)
        except ValueError:
            raise TimeoutError(
                f"Generating a string representation of {self.expr!r} took longer than {self.str_repr_timeout} seconds",
            ) from None

    def __repr__(self):
        return f"{self.__class__.__name__}(expr={self.expr!r})"
