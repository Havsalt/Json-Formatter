from annotations import Converter as _Converter


_EMPTY = ""
_KEBAB = "-"
_TAIL = "_"
_NORM_SUFFIX = "_norm"


def get_default_converter() -> _Converter:
    return norm


def get_norm_converter(function: _Converter) -> _Converter:
    # NOTE: globals from this' module namespace
    return globals().get(function.__name__ + _NORM_SUFFIX, get_default_converter())


def norm(string: str) -> str:
    return (string.replace(2*_KEBAB, _KEBAB)
                  .replace(2*_KEBAB, _KEBAB)
                  .replace(2*_TAIL, _TAIL)
                  .replace(2*_TAIL, _TAIL)
                  .strip(_KEBAB + _TAIL))


def snake(string: str) -> str:
    if string == _EMPTY:
        return string
    is_pascal_or_upper = string[0].isupper()
    final = ""
    for idx, char in enumerate(string.replace(_KEBAB, _TAIL)):
        if idx != 0 and idx != len(string) -1:
            if not is_pascal_or_upper and char.isupper():
                final += _TAIL
        final += char.lower()
    return final


def snake_norm(string: str) -> str:
    return (snake(string).replace(_KEBAB, _TAIL)
                         .replace(2*_TAIL, _TAIL)
                         .replace(2*_TAIL, _TAIL)
                         .strip(_KEBAB + _TAIL))


def camal(string: str) -> str:
    final = ""
    was_binder = False
    for idx, char in enumerate(string):
        if idx != 0:
            if char == _TAIL or char == _KEBAB:
                was_binder = True
                continue
        if was_binder:
            was_binder = False
            final += char.upper()
        elif idx == 0:
            final += char.lower()
        else:
            final += char
    return final
    

def camal_norm(string: str) -> str:
    return camal(string).strip(_KEBAB + _TAIL)


def kebab(string: str) -> str:
    if string == _EMPTY:
        return string
    is_pascal_or_upper = string[0].isupper()
    final = ""
    for idx, char in enumerate(string.replace(_TAIL, _KEBAB)):
        if idx != 0 and idx != len(string) -1:
            if not is_pascal_or_upper and char.isupper():
                final += _KEBAB
        final += char.lower()
    return final


def kebab_norm(string: str) -> str:
    return (kebab(string).replace(2*_KEBAB, _KEBAB)
                         .replace(2*_KEBAB, _KEBAB)
                         .strip(_KEBAB + _TAIL))


def pascal(string: str) -> str:
    raw = camal(string)
    if raw == _EMPTY:
        return raw
    return raw[0].upper() + raw[1:]


def pascal_norm(string: str) -> str:
    return pascal(string).strip(_KEBAB + _TAIL)
