from annotations import Converter


EMPTY = ""
KEBAB = "-"
TAIL = "_"
NORM_SUFFIX = "_norm"


def get_default_converter() -> Converter:
    return norm


def get_norm_converter(function: Converter) -> Converter:
    # NOTE: globals from this' module namespace
    return globals().get(function.__name__ + NORM_SUFFIX, get_default_converter())


def norm(string: str) -> str:
    return (string.replace(2*KEBAB, KEBAB)
                  .replace(2*KEBAB, KEBAB)
                  .replace(2*TAIL, TAIL)
                  .replace(2*TAIL, TAIL)
                  .strip(KEBAB + TAIL))


def snake(string: str) -> str:
    if string == EMPTY:
        return string
    is_pascal_or_upper = string[0].isupper()
    final = ""
    for idx, char in enumerate(string.replace(KEBAB, TAIL)):
        if idx != 0 and idx != len(string) -1:
            if not is_pascal_or_upper and char.isupper():
                final += TAIL
        final += char.lower()
    return final


def snake_norm(string: str) -> str:
    return (snake(string).replace(KEBAB, TAIL)
                         .replace(2*TAIL, TAIL)
                         .replace(2*TAIL, TAIL)
                         .strip(KEBAB + TAIL))


def camal(string: str) -> str:
    final = ""
    was_binder = False
    for idx, char in enumerate(string):
        if idx != 0:
            if char == TAIL or char == KEBAB:
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
    return camal(string).strip(KEBAB + TAIL)


def kebab(string: str) -> str:
    if string == EMPTY:
        return string
    is_pascal_or_upper = string[0].isupper()
    final = ""
    for idx, char in enumerate(string.replace(TAIL, KEBAB)):
        if idx != 0 and idx != len(string) -1:
            if not is_pascal_or_upper and char.isupper():
                final += KEBAB
        final += char.lower()
    return final


def kebab_norm(string: str) -> str:
    return (kebab(string).replace(2*KEBAB, KEBAB)
                         .replace(2*KEBAB, KEBAB)
                         .strip(KEBAB + TAIL))


def pascal(string: str) -> str:
    raw = camal(string)
    if raw == EMPTY:
        return raw
    return raw[0].upper() + raw[1:]


def pascal_norm(string: str) -> str:
    return pascal(string).strip(KEBAB + TAIL)

