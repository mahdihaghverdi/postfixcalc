from .parser import _concat_unary_minus, _syntax_check, infix_to_postfix
from .pyeval import evaluate
from .typings import ParsedPostfix, RawPostfix

got = input()
assert _syntax_check(got)
postfix: "RawPostfix" = infix_to_postfix(got)
parsed_postfix: "ParsedPostfix" = _concat_unary_minus(postfix)
print(evaluate(parsed_postfix))
