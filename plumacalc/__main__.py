from .parser import concat_unary_minus, infix_to_postfix, syntax_check
from .pyeval import evaluate
from .typings import ParsedPostfix, RawPostfix

got = input()
assert syntax_check(got)
postfix: "RawPostfix" = infix_to_postfix(got)
parsed_postfix: "ParsedPostfix" = concat_unary_minus(postfix)
print(evaluate(parsed_postfix))
