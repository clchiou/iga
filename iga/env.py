__all__ = [
    'current',
    'enter',
]

import contextlib
from collections import ChainMap

from iga.core import WriteOnceDict


_ROOT = ChainMap(WriteOnceDict())


def current():
    """Return the current environment object."""
    return current.current


current.current = _ROOT


@contextlib.contextmanager
def enter():
    """Enter a child environment context."""
    child = current.current.new_child(WriteOnceDict())
    current.current, parent = child, current.current
    yield child
    current.current = parent
