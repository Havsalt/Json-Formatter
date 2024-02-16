from argparse import Namespace as _Namespace
from typing import TypeAlias as _TypeAlias, Callable as _Callable


Converter: _TypeAlias = _Callable[[str], str]


class ParserArgs(_Namespace):
    path: str
    indent: int
    format: str | None
    norm: bool
    # NOTE: dynamic arguments can't be checked with static type checking
