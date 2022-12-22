# postfixcalc

Simple and stupid infix to postfix converter and evaluator.

# How does it work
The algorithm is very simple and straightforward

```python
from postfixcalc.pyeval import evaluate
from postfixcalc.parser import (
    extract_nums_and_ops,
    flatten_nodes,
    infix_to_postfix,
    make_num,
    parse,
    relistexpression,
)

evaluate(
    infix_to_postfix(
        make_num(
            relistexpression(
                flatten_nodes(
                    extract_nums_and_ops(
                        parse('(-1) ^ 2')
                    ),
                ),
            ),
        ),
    ),
)
```
## We should trace from bottom to top:
   1. parse the expression using `ast.parse` function. This function will parse the expression based on Python grammar and math op precedence.
   2. extract numbers, and operators outta parsed expression
   3. the extracted list contains many nested lists and tuples, so we flatten most of them
   4. we generate a better demonstration outta the flattened list
   5. we make possible strings to numbers, '-1' will be -1 and ...
   6. we generate the postfix notation outta the numbers and operators
   7. evaluate the result

But all this pain is done easily thorough `Calc` type in the library
```python
from postfixcalc import Calc

calc = Calc('(-1) ^ 2')
print(calc.answer)
```

This is easy but `Calc` type provide other _cached_propertied_ which are just the results of the upper functions
```python
from postfixcalc import Calc

c = Calc("2 * -1")
print(c.parsed)
print(c.extracted)
print(c.flattened)
print(c.strparenthesized)
print(c.listparenthesized)
print(c.numerized)
print(c.postfix)
print(c.answer)
print(c.stranswer)

# <ast.BinOp object at 0x7fcd313ecbe0>
# [([2], <ast.Mult object at 0x7fcd32002a70>, [(<ast.USub object at 0x7fcd32003010>, [1])])]
# ([2], <ast.Mult object at 0x7fcd32002a70>, (<ast.USub object at 0x7fcd32003010>, [1]))
# 2 * (-1)
# [2, '*', '(', '-1', ')']
# [2, '*', '(', -1, ')']
# [2, -1, '*']
# -2
# -2
```

# Important notes
1. For safety reasons, calculations are done with a timeout which is absolutely easy to change:
```python
c = Calc('...', timeout=10)
```
timeout is in seconds.

2. `answer` property returns the actual object of the answer, whether it is `int` or `float`, BUT if you want to `print` the answer, you should consider the `obj to str conversion` time, it may be quite long or short depending on that obj; because of this `Calc` implements a new propery called `stranswer` which calculates the str repr with a timeout and raises exceptions if it would take long
Always use `stranswer` if you want the str repr of the `answer`
