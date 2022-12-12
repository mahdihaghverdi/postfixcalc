from .parser import _syntax_check, concat_unary_minus, infix_to_postfix
from .pyeval import evaluate
from .typings import ParsedPostfix, RawPostfix

got = input()
assert _syntax_check(got)
postfix: "RawPostfix" = infix_to_postfix(got)
parsed_postfix: "ParsedPostfix" = concat_unary_minus(postfix)
print(evaluate(parsed_postfix))
