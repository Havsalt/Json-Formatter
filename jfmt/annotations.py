from argparse import Namespace as _Namespace
from typing import TypeAlias as _TypeAlias, Callable as _Callable


Converter: _TypeAlias = _Callable[[str], str]


class ParserArguments(_Namespace):
    # silent: bool
    # verbose: bool
    indent_size: int
    normalization_mode: bool
    format_rule: str | None
    path: str
    # NOTE: dynamic arguments can't be checked with static type checking
