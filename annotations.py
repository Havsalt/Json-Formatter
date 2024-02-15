from typing import TypeAlias, Callable


Converter: TypeAlias = Callable[[str], str]


class ParserArgs:
    path: str
    indent: int
    format: str | None
    norm: bool
    # NOTE: dynamic arguments can't be checked with static type checking
