"""
jfmt

Indent structure and format keys in your deeply nested .json
"""

from __future__ import annotations

__version__ = "0.4.0"

import argparse
import pathlib
import json
from typing import Any, Mapping, MutableMapping

import colex
from actus import info, error, LogSection, Style

from .converters import (
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
from .annotations import Converter, ParserArguments


info.set_style(Style(
    label=colex.BLUE,
    highlight=colex.PURPLE
))
reason = LogSection("Reason", style=Style(
    label=colex.ORANGE,
    text=colex.YELLOW
))

converter_functions: list[Converter] = [
    str.lower,
    str.upper,
    str.title,
    snake,
    camal,
    kebab,
    pascal
]


def convert_keys_into(converter: Converter, mapping: Mapping[str, Any], buffer: MutableMapping[str, Any]) -> None:
    for key, value in mapping.items():
        if isinstance(value, dict):
            buffer[converter(key)] = dict()
            convert_keys_into(converter, value, buffer[converter(key)])
        else:
            buffer[converter(key)] = value


def main() -> int:
    converter_mappings: dict[str, Converter] = {
        function.__name__: function for function in converter_functions
    }
    parser = argparse.ArgumentParser(
        prog="jfmt",
        description="Formats the given file to use indents, and can convert keys to lowercase",
        add_help=False
    )
    parser.add_argument(
        "-h", "--help",
        action="help",
        help="Show this help message and exit",
        default=argparse.SUPPRESS
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s: v{__version__}",
        help="Show `%(prog)s` version number and exit"
    )
    # print_group = parser.add_mutually_exclusive_group()
    # print_group.add_argument(
    #     "--verbose",
    #     action="store_true",
    #     help="Display more info during execution"
    # )
    # print_group.add_argument(
    #     "--silent",
    #     action="store_true",
    #     help="Display less info during execution"
    # )
    parser.add_argument(
        "-i", "--indent",
        type=int,
        default=2,
        metavar="[size]",
        dest="indent_size",
        help="Indentation size given in spaces. Defaults to 2"
    )
    parser.add_argument(
        "-n", "--norm",
        action="store_true",
        dest="normalization_mode",
        help="Normalize duplicate delimiters"
    )
    format_action = parser.add_argument(
        "-f", "--format",
        choices=converter_mappings.keys(),
        metavar="{" + ", ".join(converter_mappings.keys()) + "}", # adds space after comma
        dest="format_rule",
        help="Select method used to convert keys"
    )
    parser.add_argument(
        "path",
        help="Path to .json file"
    )

    for function in converter_functions:
        char = function.__name__[0]
        name = function.__name__
        parser.add_argument(
            f"-{char}", f"--{name}",
            action="store_true",
            help=f"Convert keys to {name}"
        )
    args = ParserArguments()
    parser.parse_args(namespace=args)

    full_path = pathlib.Path(args.path).resolve()

    if not full_path.exists():
        error(f"Invalid path $[{full_path}]")
        return 1 # invalid path
    elif not full_path.is_file():
        error(f"Path is not a file $[{full_path}]")
        return 2 # not a file

    read_fd = full_path.open(encoding="utf-8")
    try:
        data: dict[str, Any] = json.load(read_fd)
    except json.decoder.JSONDecodeError as exception:
        error(f"Error while parsing: $[{exception.__class__.__name__}]")
        reason(exception.msg)
        info(
            f"Problem at line $[{exception.lineno}],",
            f"column $[{exception.colno}]",
            f"(char $[{exception.pos}])"
        )
        return 3 # json could not be decoded
    finally:
        read_fd.close()

    assert format_action.choices is not None
    
    if args.format_rule is not None:
        format_flags_present: list[str] = [
            f"--{choice}"
            for choice in format_action.choices
            if getattr(args, choice) == True
        ]
        if format_flags_present:
            error(
                f"Conflicting flags: $[--{args.format_rule}],",
                f"$[{', '.join(format_flags_present)}]"
            )
            return 4 # conflicting flags
        result: dict[str, Any] = dict()
        converter = converter_mappings[args.format_rule]
        if args.normalization_mode:
            converter: Converter = globals().get(f"{converter.__name__}_norm", converter)
        convert_keys_into(converter, data, result)
        data = result
    else:
        n_format_flags = sum(int(getattr(args, choice)) for choice in format_action.choices)
        if n_format_flags == 0:
            if args.normalization_mode:
                result: dict[str, Any] = dict()
                converter = get_default_converter()
                convert_keys_into(converter, data, result)
                data = result
        elif n_format_flags != 1:
            format_flags_present: list[str] = [
                f"--{choice}"
                for choice in format_action.choices
                if getattr(args, choice) == True
            ]
            error(
                f"Multiple format flags not allowed:",
                f"$[{', '.join(format_flags_present)}]"
            )
            return 4 # conflicting flags
        else:
            result: dict[str, Any] = dict()
            converter = [
                converter_mappings[choice]
                for choice in format_action.choices
                if getattr(args, choice) == True
            ][0] # take first element, should only be 1 present
            if args.normalization_mode:
                converter = get_norm_converter(converter)
            convert_keys_into(converter, data, result)
            data = result

    # save result to file
    fd = full_path.open(mode="w", encoding="utf-8")
    json.dump(data, fd, indent=args.indent_size)
    fd.close()

    return 0
