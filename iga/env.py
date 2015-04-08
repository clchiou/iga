__all__ = [
    'current',
    'root',
    'enter_child_env',
]

import contextlib
from collections import ChainMap

from iga.core import WriteOnceDict


_ROOT = ChainMap(WriteOnceDict())


def current():
    """Return the current env object."""
    return current.current


current.current = _ROOT


@contextlib.contextmanager
def enter_child_env():
    """Enter a child env context."""
    child = current.current.new_child(WriteOnceDict())
    current.current, parent = child, current.current
    yield child
    current.current = parent


def root():
    """Return the singleton root env object."""
    return _ROOT
