__all__ = [
    'current',
    'root',
    'enter_child_env',
]

import contextlib
import threading
from collections import ChainMap

from iga.core import WriteOnceDict


_LOCAL = None
_ROOT = None


def _local():
    global _LOCAL
    if _LOCAL is None:
        _LOCAL = threading.local()
    if not hasattr(_LOCAL, 'current'):
        _LOCAL.current = root()
    return _LOCAL


def root():
    """Return the singleton root env object."""
    global _ROOT
    if _ROOT is None:
        _ROOT = ChainMap(WriteOnceDict())
    return _ROOT


def current():
    """Return the current env object."""
    return _local().current


@contextlib.contextmanager
def enter_child_env():
    """Enter a child env context."""
    local = _local()
    child = local.current.new_child(WriteOnceDict())
    local.current, parent = child, local.current
    yield child
    local.current = parent
