"""File path utilities."""

__all__ = [
    'PathGlob',
    'get_caller_path',
]

import inspect
from pathlib import Path

from iga.error import IgaError


class PathGlob: pass


def get_caller_path(ancestor):
    """Return the file path of i-th ancestor of the caller.

    The zero-th ancestor is the caller, first ancestor is caller's
    caller, and so on.
    """
    call_stack = inspect.stack(context=0)
    if call_stack is None:
        raise IgaError('inspect is not supported')
    return Path.cwd() / call_stack[1 + ancestor][1]
