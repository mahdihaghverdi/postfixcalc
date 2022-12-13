from ast import Add, Sub, Mult, Div, Pow, USub, UAdd
from typing import TypeAlias, Type, Any

ast_ops = Type[Add | Sub | Mult | Div | Pow | USub | UAdd]
ListExpression: TypeAlias = list[int | float | tuple | list | ast_ops]
TupleExpression: TypeAlias = tuple[list | tuple[Any] | Any, ...]
ListPostfix: TypeAlias = list[str | float | int]