"""Execution context."""

__all__ = [
    'get_context',
    'new_context',
]

import contextlib
from collections import ChainMap

from iga.core import WriteOnceDict


_CONTEXT = ChainMap(WriteOnceDict())
_current = _CONTEXT


def get_context():
    """Return the execution context."""
    return _current


@contextlib.contextmanager
def new_context(**kwargs):
    """Create a new level of context."""
    global _current
    previous = _current
    _current = _current.new_child(WriteOnceDict(kwargs))
    yield _current
    _current = previous
