__version__ = "0.3.0"

import argparse
import pathlib
import json
from typing import Any, Mapping, MutableMapping
from converters import (
    get_default_converter,
    get_norm_converter,
    snake,
    snake_norm,
    camal,
    camal_norm,
    kebab,
    kebab_norm,
    pascal,
    pascal_norm
)
from annotations import Converter, ParserArgs


RESET = "\u001b[0m"
BRIGHT = "\u001b[;1m"
WHITE = "\u001b[37m"
RED = "\u001b[31m"
YELLOW = "\u001b[33m"
BLUE = "\u001b[34m"
PURPLE = "\u001b[35m"
CYAN = "\u001b[36m"
ORANGE = "\u001b[38;5;214m"

converter_functions: list[Converter] = [
    str.lower,
    str.upper,
    str.title,
    snake,
    camal,
    kebab,
    pascal
]
default_converter: Converter = snake
converter_mappings: dict[str, Converter] = {
    function.__name__: function for function in converter_functions
}

parser = argparse.ArgumentParser(
    prog="JSON Formatter",
    description="Formats the given file to use indents, and can convert keys to lowercase"
    )
parser.add_argument("path")
parser.add_argument("-v", "--version",
                    action="version",
                    version=f"%(prog)s: v{__version__}")
parser.add_argument("-i", "--indent",
                    type=int,
                    default=2,
                    help="Indentation level given in spaces")
norm_action = parser.add_argument("-n", "--norm",
                    action="store_true",
                    help="Normalize duplicate delimiters")
format_action = parser.add_argument("-f", "--format",
                    choices=converter_mappings.keys(),
                    help="Select method used to convert keys")
for function in converter_functions:
    char = function.__name__[0]
    name = function.__name__
    parser.add_argument(f"-{char}", f"--{name}",
                        action="store_true",
                        help=f"Convert keys to {name}")
args = parser.parse_args() # type: ParserArgs  # type: ignore

full_path = pathlib.Path(args.path).resolve()

read_file = open(full_path, "r", encoding="utf-8")
try:
    data: dict[str, Any] = json.load(read_file)
except json.decoder.JSONDecodeError as error:
    error_header = f"{BRIGHT}{WHITE}{error.__class__.__name__}{RESET}{WHITE}"
    if not error.__class__.__name__.lower().endswith("error"):
        error_header += " error"
    error_header += " while parsing:"
    error_message = "\n".join((
        f"{BRIGHT}{RED}[Error]{RESET} {error_header}",
        f"  {BRIGHT}{ORANGE}[Message]{RESET} {YELLOW}{error.msg}{RESET}",
        f"  {BRIGHT}{BLUE}[Located]{RESET} {WHITE}line {PURPLE}{error.lineno}{WHITE}, column {PURPLE}{error.colno} {RESET}(char {CYAN}{error.pos}{RESET})"
    ))
    print(error_message)
    exit()
finally:
    read_file.close()


def convert_keys_into(converter: Converter, mapping: Mapping[str, Any], buffer: MutableMapping[str, Any]) -> None:
    for key, value in mapping.items():
        if isinstance(value, dict):
            buffer[converter(key)] = dict()
            convert_keys_into(converter, value, buffer[converter(key)])
        else:
            buffer[converter(key)] = value


assert format_action.choices is not None
if args.format is not None:
    format_flags_present: list[str] = [
        f"--{choice}"
        for choice in format_action.choices
        if getattr(args, choice) == True
    ]
    if format_flags_present:
        parser.error(f"conflicting flags: --{args.format}, {', '.join(format_flags_present)}")
    result: dict[str, Any] = dict()
    converter = converter_mappings[args.format]
    if args.norm:
        converter: Converter = globals().get(f"{converter.__name__}_norm", converter)
    convert_keys_into(converter, data, result)
    data = result
else:
    n_format_flags = sum(int(getattr(args, choice)) for choice in format_action.choices)
    if n_format_flags == 0:
        if args.norm:
            result: dict[str, Any] = dict()
            converter = get_default_converter()
            convert_keys_into(converter, data, result)
            data = result
        else:
            parser.error(f"format flag not present while not using {norm_action.choices}")
    elif n_format_flags != 1:
        format_flags_present: list[str] = [
            f"--{choice}"
            for choice in format_action.choices
            if getattr(args, choice) == True
        ]
        parser.error(f"multiple format flags not allowed: {', '.join(format_flags_present)}")
    else:
        result: dict[str, Any] = dict()
        converter = [
            converter_mappings[choice]
            for choice in format_action.choices
            if getattr(args, choice) == True
        ][0] # take first element, should only be 1 present
        if args.norm:
            converter = get_norm_converter(converter)
        convert_keys_into(converter, data, result)
        data = result

# save result to file
string_result = json.dumps(data, indent=args.indent)
write_file = open(full_path, "w", encoding="utf-8")
write_file.write(string_result)
write_file.close()
