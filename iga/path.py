"""File path utilities."""

__all__ = [
    'Glob',
    'get_caller_path',
]

import inspect
from pathlib import Path

import iga.fargparse
from iga.error import IgaError


class Glob:
    """Keep a glob pattern before we have a Path object."""

    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, path):
        return path.match(self.pattern)

    def glob(self, from_path):
        yield from from_path.glob(self.pattern)


iga.fargparse.Parser.register_parse_func(Glob, Glob)


def get_caller_path(ancestor):
    """Return the file path of i-th ancestor of the caller.

    The zero-th ancestor is the caller, first ancestor is caller's
    caller, and so on.
    """
    call_stack = inspect.stack(context=0)
    if call_stack is None:
        raise IgaError('inspect is not supported')
    return Path.cwd() / call_stack[1 + ancestor][1]
