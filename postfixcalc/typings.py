from ast import Add, Div, Mult, Pow, Sub, UAdd, USub
from numbers import Number
from typing import Any, Type, TypeAlias

ast_ops = Type[Add | Sub | Mult | Div | Pow | USub | UAdd]
ListExpression: TypeAlias = list[int | float | tuple | list | ast_ops]
TupleExpression: TypeAlias = tuple[list | tuple[Any] | Any, ...]
ListPostfix: TypeAlias = list[str | Number]
