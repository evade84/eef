import sys
from typing import Union, Optional

from typer import echo, style


def error(message: str, terminate: bool = False):
    echo(f"{style('Error:', fg='red')} {message}", err=True)
    if terminate:
        sys.exit(-1)


def info(message: str, terminate: bool = False):
    echo(message)
    if terminate:
        sys.exit()


def pretty_address(address: str):
    return style(address, italic=True)


def pretty_description(description: str):
    return (
        style(description, italic=True)
        if description
        else style("<no description>", dim=True)
    )


def pretty_tag(tag: str):
    return style(tag, underline=True) if tag else style("<no tag>", dim=True)


def pretty_signature(signature: str):
    return style(signature) if signature else style("<no signature>", dim=True)


def pretty_bool(x: bool, invert: bool = False):
    if x:
        return style("yes", fg="green" if not invert else "red")
    else:
        return style("no", fg="red" if not invert else "green")


def pretty_first_last(first: Optional[int] = None, last: Optional[int] = None):
    if first:
        return "first"
    elif last:
        return "last"
    else:
        raise ValueError()
